class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not hasattr(self, 'settings'):
            self.settings = {
                "DEFAULT_PAGE_SIZE": 20,
                "ENABLE_ANALYTICS": True,
                "RATE_LIMIT": 100
            }

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value