class Config(dict):
    """A dictionary that allows attribute-style access."""

    def __init__(self, yaml_data: dict = None):
        super().__init__()
        # Default attributes
        self.logs_dir = "/tmp"
        self.browser = 'chrome'
        self.remote_webdriver_url = None
        self.screen_resolution = '800x600'
        self.global_timeout = 5
        self.headless = False
        # Update with provided values
        self.update(yaml_data)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f'Config has no "{key}"')

    def __setattr__(self, key, value):
        self[key] = value
