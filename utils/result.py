class Result:
    """Class to represent the result of a UI or API call."""

    def __init__(self, success: bool = False, data=None, error_msg=None):
        self.success = success
        self.data = data
        self.error_msg = error_msg
