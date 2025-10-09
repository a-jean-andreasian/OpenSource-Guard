import typing
if typing.TYPE_CHECKING:
    from open_source_guard.src.jobs.responses import SingleJobResult


class JobManagerResult:
    def __init__(
        self,
        status: bool,
        failed_jobs: list["SingleJobResult"] = None,
        msg: str = None
    ):
        self.status = status
        self.failed_jobs = failed_jobs
        self.msg = msg
