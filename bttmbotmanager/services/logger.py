import logging
import sys

from bttmbotmanager import settings

datefmt = "%Y-%m-%d %H:%M:%S"
logFormatter = logging.Formatter(
    "[%(levelname)s] [%(threadName)s] %(asctime)s - %(message)s", datefmt=datefmt
)
level = logging.getLevelName(settings.log_level)

logger = logging.getLogger(__name__)
logger.setLevel(level)

fileHandler = logging.FileHandler("{0}.log".format("autotrading"))
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(level)

logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(level)
logger.addHandler(consoleHandler)
