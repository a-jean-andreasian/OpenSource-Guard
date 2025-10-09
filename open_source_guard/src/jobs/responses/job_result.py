import typing


class SingleJobResult:
    """
    Response for a single job returned by a job function.
    """

    def __init__(self, job: typing.Callable, status: bool, msg: str = ""):
        self.status = status
        self.msg = msg
        self.job = job

    def __bool__(self):
        return self.status
