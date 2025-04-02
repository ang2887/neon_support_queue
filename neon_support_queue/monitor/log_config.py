# log_config.py v2

from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import logging

class ComboRotatingHandler(logging.Handler):
    def __init__(self, filename, maxBytes=512000, backupCount=5):
        super().__init__()
        self.size_handler = RotatingFileHandler(
            filename, maxBytes=maxBytes, backupCount=backupCount, encoding='utf-8'
        )
        self.time_handler = TimedRotatingFileHandler(
            filename, when="midnight", backupCount=backupCount, encoding='utf-8'
        )

    def emit(self, record):
        self.size_handler.emit(record)
        self.time_handler.emit(record)
def setup_logger(log_name):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    log_file = f"{log_name}.log"

    handler = ComboRotatingHandler(log_file)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(name)s]: %(message)s")

    # ✅ Apply formatter to internal handlers
    handler.size_handler.setFormatter(formatter)
    handler.time_handler.setFormatter(formatter)

    # ✅ Also apply to stream (console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)
    logger.addHandler(stream_handler)

    return logger