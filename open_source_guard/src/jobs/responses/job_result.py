class JobResult:
    def __init__(self, status: bool, msg: str = ""):
        self.status = status
        self.msg = msg

    def __bool__(self):
        return self.status
