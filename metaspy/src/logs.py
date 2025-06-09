import logging
from .config import Config

class LogsAdapter(logging.LoggerAdapter):
    """Logs adapter class"""
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})
    def log_error(self, message):
        """Logs error message safely"""
        # Escape or sanitize message to prevent log injection
        safe_message = str(message).replace("\n", "\\n").replace("\r", "\\r")
        self.error("Error occurred: %s", safe_message)
# Initialize logger instance
logger = logging.getLogger("logger")
logger.setLevel(logging.ERROR)
# Configure file handler
file_handler = logging.FileHandler(Config.LOG_FILE_PATH)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
# Create instance of LogsAdapter
logs = LogsAdapter(logger)