import logging


def configure_logger(name):
    logger = logging.getLogger(name)
    logger.propagate = (
        False  # Prevents log messages from being passed to the parent logger
    )
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

    file_handler = logging.FileHandler("scraper.log")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger
