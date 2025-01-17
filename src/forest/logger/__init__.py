import logging.handlers
import os
import logging
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y_%M%H%S')}.log"

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    format="[%(asctime)s] %(lineno)d - %(levelname)s %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)
