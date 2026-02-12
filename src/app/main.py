import logging
from dotenv import load_dotenv
load_dotenv()
import os
import uvicorn
from src.app.interface.fastapi.server import create_fastapi_server
from src.broker.setup import setup_broker
from src.di.setup import setup_dependencies


def main():
    level = os.getenv("LOGGER_LEVEL", logging.INFO)
  
    logging.basicConfig(
        level=int(level),
        format="%(levelname)s - %(name)s - %(message)s"
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)
    logging.getLogger("aiormq.connection").setLevel(logging.WARNING)
    logging.getLogger("aio_pika").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.debug("!!!!! LOGGER LEVEL SET TO DEBUG !!!!!")


    app = create_fastapi_server()
    setup_dependencies()
    # setup_broker()
    
    port = os.getenv("PORT", 8000)
    concurrency_limit = os.getenv("CONCURRENCY_LIMIT", 100)
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=int(port),
        workers=1,
        access_log=False,  
        limit_concurrency=concurrency_limit,  
        timeout_keep_alive=30
    )

if __name__ == "__main__":
    main()