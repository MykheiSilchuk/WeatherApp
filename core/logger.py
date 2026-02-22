import logging


def setup_logger():

    logger = logging.getLogger("WeatherApp")

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


class AppLogger:

    def __init__(self):
        self.logger = setup_logger()

    def debug(self, msg, exc_info=False):
        self.logger.debug(msg, exc_info=exc_info)

    def info(self, msg, exc_info=False):
        self.logger.info(msg, exc_info=exc_info)

    def warning(self, msg, exc_info=False):
        self.logger.warning(msg, exc_info=exc_info)

    def error(self, msg, exc_info=False):
        self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg, exc_info=False):
        self.logger.critical(msg, exc_info=exc_info)


app_logger = AppLogger()