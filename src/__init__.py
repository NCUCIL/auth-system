from dotenv import load_dotenv

load_dotenv()

import os
from .config import config, BaseConfig

CONFIG: BaseConfig = config.get(os.getenv("STAGE", "DEV"))