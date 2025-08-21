from utils.result import Result


class AnyOtherServiceApi:

    def __init__(self, api_crud):
        self.api = api_crud

    def do_something(self) -> Result:
        raise NotImplementedError()
