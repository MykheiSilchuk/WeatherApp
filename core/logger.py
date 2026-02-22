import logging
import os


def setup_logger():

    logger = logging.getLogger("WeatherApp")

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Logs path
    log_dir = "logs/"
    log_file = os.path.join(log_dir, "app.log")

    # Creating directory if not exist 
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

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