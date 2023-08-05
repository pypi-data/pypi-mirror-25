import asyncio
import asyncio.subprocess
import logging
import os
import sys
import time
from email.mime.text import MIMEText
from typing import Any, Awaitable, Dict, List, Optional  # noqa
from enum import Enum

from raven import Client
from raven_aiohttp import AioHttpTransport

import aiosmtplib
from yacron.config import JobConfig

logger = logging.getLogger('yacron')


def create_task(coro: Awaitable) -> asyncio.Task:
    return asyncio.get_event_loop().create_task(coro)


class ReportType(Enum):
    FAILURE = 1
    SUCCESS = 2


class StreamReader:

    def __init__(self,
                 job_name: str,
                 stream_name: str,
                 stream: asyncio.StreamReader,
                 save_limit: int) -> None:
        self.save_top = []  # type: List[str]
        self.save_bottom = []  # type: List[str]
        self.job_name = job_name
        self.save_limit = save_limit
        self.stream_name = stream_name
        self._reader = create_task(self._read(stream))
        self.discarded_lines = 0

    async def _read(self, stream):
        prefix = "[{} {}] ".format(self.job_name, self.stream_name)
        limit_top = self.save_limit // 2
        limit_bottom = self.save_limit - limit_top
        while True:
            line = (await stream.readline()).decode("utf-8")
            if not line:
                return
            sys.stdout.write(prefix + line)
            sys.stdout.flush()
            if len(self.save_top) < limit_top:
                self.save_top.append(line)
            else:
                if len(self.save_bottom) == limit_bottom:
                    del self.save_bottom[0]
                    self.discarded_lines += 1
                self.save_bottom.append(line)

    async def join(self) -> str:
        await self._reader
        if self.save_bottom:
            middle = (["   [.... {} lines discarded ...]\n"
                       .format(self.discarded_lines)]
                      if self.discarded_lines else [])
            output = ''.join(self.save_top + middle + self.save_bottom)
        else:
            output = ''.join(self.save_top)
        return output


class Reporter:

    async def report(self, report_type: ReportType, job: 'RunningJob',
                     config: Dict[str, Any]) -> None:
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def _format_body(job):
        if job.stdout and job.stderr:
            body = ("STDOUT:\n---\n{}\n---\nSTDERR:\n{}"
                    .format(job.stdout, job.stderr))
        else:
            body = job.stdout or job.stderr or '(no output was captured)'
        return body


class SentryReporter(Reporter):

    async def report(self, report_type: ReportType, job: 'RunningJob',
                     config: Dict[str, Any]) -> None:
        config = config['sentry']
        if config['dsn']['value']:
            dsn = config['dsn']['value']
        elif config['dsn']['fromFile']:
            with open(config['dsn']['fromFile'], "rt") as dsn_file:
                dsn = dsn_file.read().strip()
        elif config['dsn']['fromEnvVar']:
            dsn = os.environ[config['dsn']['fromEnvVar']]
        else:
            return  # sentry disabled: early return

        body = self._format_body(job)

        if report_type == ReportType.SUCCESS:
            headline = ('Cron job {!r} completed'
                        .format(job.config.name))
        elif report_type == ReportType.FAILURE:
            headline = ('Cron job {!r} failed'
                        .format(job.config.name))
        body = "{}\n\n{}".format(headline, body)

        client = Client(transport=AioHttpTransport,
                        dsn=dsn,
                        string_max_length=4096)
        extra = {
            'job': job.config.name,
            'exit_code': job.retcode,
            'command': job.config.command,
            'shell': job.config.shell,
            'success': True if report_type == ReportType.SUCCESS else False,
        }
        logger.debug("sentry body: %r", body)
        client.captureMessage(
            body,
            extra=extra,
        )


class MailReporter(Reporter):

    async def report(self, report_type: ReportType, job: 'RunningJob',
                     config: Dict[str, Any]) -> None:
        mail = config['mail']
        if not ((mail['smtpHost'] or mail['smtp_host']) and
                mail['to'] and mail['from']):
            return  # email reporting disabled

        body = self._format_body(job)

        if mail['smtpHost']:
            smtp_host = mail['smtpHost']
        else:  # pragma: no cover
            logger.warning("smtp_host is deprecated, was renamed to smtpHost")
            smtp_host = mail['smtp_host']
        if mail['smtpPort']:
            smtp_port = mail['smtpPort']
        else:  # pragma: no cover
            logger.warning("smtp_port is deprecated, was renamed to smtpPort")
            smtp_port = mail['smtp_port']

        logger.debug("smtp: host=%r, port=%r", smtp_host, smtp_port)
        smtp = aiosmtplib.SMTP(hostname=smtp_host, port=smtp_port)
        await smtp.connect()
        message = MIMEText(body)
        message['From'] = mail['from']
        message['To'] = mail['to']
        if report_type == ReportType.SUCCESS:
            message['Subject'] = ('Cron job {!r} completed'
                                  .format(job.config.name))
        elif report_type == ReportType.FAILURE:
            message['Subject'] = ('Cron job {!r} failed'
                                  .format(job.config.name))
        else:  # pragma: no cover
            raise AssertionError
        await smtp.send_message(message)


class JobRetryState:

    def __init__(self, initial_delay: float,
                 multiplier: float,
                 max_delay: float) -> None:
        self.multiplier = multiplier
        self.max_delay = max_delay
        self.delay = initial_delay
        self.count = 0  # number of times retried
        self.task = None  # type: Optional[asyncio.Task]
        self.cancelled = False

    def next_delay(self) -> float:
        delay = self.delay
        self.delay = min(delay * self.multiplier, self.max_delay)
        self.count += 1
        return delay


class RunningJob:
    REPORTERS = [
        SentryReporter(),
        MailReporter(),
    ]  # type: List[Reporter]

    def __init__(self, config: JobConfig,
                 retry_state: Optional[JobRetryState]) -> None:
        self.config = config
        self.proc = None  # type: Optional[asyncio.subprocess.Process]
        self.retcode = None  # type: Optional[int]
        self._stderr_reader = None  # type: Optional[StreamReader]
        self._stdout_reader = None  # type: Optional[StreamReader]
        self.stderr = None  # type: Optional[str]
        self.stdout = None  # type: Optional[str]
        self.execution_deadline = None  # type: Optional[float]
        self.retry_state = retry_state

    async def start(self) -> None:
        if self.proc is not None:
            raise RuntimeError("process already running")
        kwargs = {}  # type: Dict[str, Any]
        if isinstance(self.config.command, list):
            create = asyncio.create_subprocess_exec
            cmd = self.config.command
        else:
            if self.config.shell:
                create = asyncio.create_subprocess_exec
                cmd = [self.config.shell, '-c', self.config.command]
            else:
                create = asyncio.create_subprocess_shell
                cmd = [self.config.command]
        if self.config.environment:
            env = dict(os.environ)
            for envvar in self.config.environment:
                env[envvar['key']] = envvar['value']
            kwargs['env'] = env
        logger.debug("%s: will execute argv %r", self.config.name, cmd)
        if self.config.captureStderr:
            kwargs['stderr'] = asyncio.subprocess.PIPE
        if self.config.captureStdout:
            kwargs['stdout'] = asyncio.subprocess.PIPE
        if self.config.executionTimeout:
            self.execution_deadline = (time.perf_counter() +
                                       self.config.executionTimeout)

        self.proc = await create(*cmd, **kwargs)

        if self.config.captureStderr:
            assert self.proc.stderr is not None
            self._stderr_reader = \
                StreamReader(self.config.name, 'stderr', self.proc.stderr,
                             self.config.saveLimit)
        if self.config.captureStdout:
            assert self.proc.stdout is not None
            self._stdout_reader = \
                StreamReader(self.config.name, 'stdout', self.proc.stdout,
                             self.config.saveLimit)

    async def wait(self) -> None:
        if self.proc is None:
            raise RuntimeError("process is not running")
        if self.execution_deadline is None:
            self.retcode = await self.proc.wait()
        else:
            timeout = self.execution_deadline - time.perf_counter()
            try:
                if timeout > 0:
                    self.retcode = await asyncio.wait_for(
                        self.proc.wait(),
                        timeout,
                    )
                else:
                    raise asyncio.TimeoutError
            except asyncio.TimeoutError:
                logger.info("Job %s exceeded its executionTimeout of "
                            "%.1f seconds, cancelling it...",
                            self.config.name, self.config.executionTimeout)
                self.retcode = -100
                await self.cancel()
        if self._stderr_reader:
            self.stderr = await self._stderr_reader.join()
        if self._stdout_reader:
            self.stdout = await self._stdout_reader.join()

    @property
    def failed(self) -> bool:
        if self.config.failsWhen['nonzeroReturn'] and self.retcode != 0:
            return True
        if self.config.failsWhen['producesStdout'] and self.stdout:
            return True
        if self.config.failsWhen['producesStderr'] and self.stderr:
            return True
        return False

    async def cancel(self) -> None:
        if self.proc is None:
            raise RuntimeError("process is not running")
        self.proc.terminate()
        try:
            await asyncio.wait_for(self.proc.wait(), self.config.killTimeout)
        except asyncio.TimeoutError:
            logger.warning("Job %s did not gracefully terminate after "
                           "%.1f seconds, killing it...",
                           self.config.name, self.config.killTimeout)
            self.proc.kill()

    async def report_failure(self):
        logger.info("Cron job %s: reporting failure", self.config.name)
        await self._report_common(self.config.onFailure['report'],
                                  ReportType.FAILURE)

    async def report_permanent_failure(self):
        logger.info("Cron job %s: reporting permanent failure",
                    self.config.name)
        await self._report_common(self.config.onPermanentFailure['report'],
                                  ReportType.FAILURE)

    async def report_success(self):
        logger.info("Cron job %s: reporting success", self.config.name)
        await self._report_common(self.config.onSuccess['report'],
                                  ReportType.SUCCESS)

    async def _report_common(self, report_config: dict,
                             report_type: ReportType) -> None:
        results = await asyncio.gather(
            *[reporter.report(report_type, self, report_config)
              for reporter in self.REPORTERS],
            return_exceptions=True
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error("Problem reporting job %s failure: %s",
                             self.config.name, result)
