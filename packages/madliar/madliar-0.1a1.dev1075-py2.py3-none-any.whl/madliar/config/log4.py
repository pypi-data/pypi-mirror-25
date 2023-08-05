import os
import logging
from madliar.config import settings


__all__ = ("logger", )

logger = logging.getLogger("madliar")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(settings.SYS_LOG_PATH, "madliar_debug.log"))
formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s:%(lineno)d:%(funcName)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
