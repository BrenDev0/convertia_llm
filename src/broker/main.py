import asyncio
import logging
import os
from dotenv import load_dotenv

from src.di.injector import Injector
from src.broker.setup import setup_dependencies, setup_broker

load_dotenv()

logging.basicConfig(
    level=int(os.getenv("LOGGER_LEVEL", logging.INFO)),
    format="%(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def main():
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)
    logging.getLogger("aiormq.connection").setLevel(logging.WARNING)
    logging.getLogger("aio_pika").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.debug("!!!!! LOGGER LEVEL SET TO DEBUG !!!!!")
    logger.info("Starting broker service...")

    injector = Injector()

    setup_dependencies(injector)
   
    await setup_broker(injector)

    logger.info("Broker is running")

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
