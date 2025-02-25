import logging

class LoggerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggerSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger("connectly_logger")
            self.logger.setLevel(logging.INFO)  # Set the logging level
            if not self.logger.handlers:  # Prevent duplicate handlers
                handler = logging.StreamHandler()
                formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger