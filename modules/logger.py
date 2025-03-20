from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging import  Formatter, getLogger, StreamHandler

class Logger:
    def __init__(self, log_level=DEBUG):
        self.logger = getLogger(__name__)
        self.logger.setLevel(log_level)

        handler = StreamHandler()
        handler.setLevel(log_level)
        formatter = Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

if __name__ == "__main__":
    logger = Logger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
