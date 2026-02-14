import logging
from dotenv import load_dotenv
load_dotenv()
import os
from src.app.interface.fastapi.server import create_fastapi_server

level = os.getenv("LOGGER_LEVEL", logging.INFO)

logging.basicConfig(
    level=int(level),
    format="%(levelname)s - %(name)s - %(message)s"
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
logging.getLogger("aiormq.connection").setLevel(logging.WARNING)
logging.getLogger("aio_pika").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.debug("!!!!! LOGGER LEVEL SET TO DEBUG !!!!!")

app = create_fastapi_server()
