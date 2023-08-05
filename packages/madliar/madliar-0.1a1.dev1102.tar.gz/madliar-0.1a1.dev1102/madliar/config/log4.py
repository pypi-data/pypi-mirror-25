import os
from madliar.config import settings


def make_logger(name, log_file_path, level="DEBUG", log_format=None):
    import logging
    if not log_format:
        log_format = "%(levelname)s %(asctime)s: %(message)s"

    level_names = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARN": logging.WARNING,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET,
    }

    fh = logging.FileHandler(log_file_path)
    fh.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(name)
    logger.setLevel(level_names.get(level.upper(), logging.DEBUG))
    logger.addHandler(fh)
    return logger


logging = make_logger(
    name="madliar",
    log_file_path=os.path.join(settings.SYS_LOG_PATH, "madliar_sys.log"),
    level="INFO",
)
