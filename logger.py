import logging
import os
from logging.handlers import RotatingFileHandler

log = logging.getLogger(__name__)
FORMAT = "%(asctime)s | %(levelname)s | [%(filename)s->%(funcName)s():%(lineno)s] | %(message)s"

logging.basicConfig(force=True, datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

# Log to file
logging_filename = os.path.join("data_safe_guard.log")
handler = RotatingFileHandler(logging_filename, maxBytes=1000000, backupCount=10)  # 10 files of 1MB each
handler.setFormatter(logging.Formatter(FORMAT))
log.addHandler(handler)