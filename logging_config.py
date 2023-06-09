import logging
from pytz import timezone
from datetime import datetime


class CustomFormatter:
    def __init__(self):
        self.formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        self.oslo_tz = timezone("Europe/Oslo")

    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return self.oslo_tz.localize(dt)

    def format(self, record):
        # Modify record's asctime with our custom format
        record.asctime = self.formatTime(record)
        return self.formatter.format(record)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec="milliseconds")
            except TypeError:
                s = dt.isoformat()
        return s


def configure_logger(name, log_path):
    logger = logging.getLogger(name)
    logger.propagate = (
        False  # Prevents log messages from being passed to the parent logger
    )

    formatter = CustomFormatter()

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger
