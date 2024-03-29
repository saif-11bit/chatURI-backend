"""" main app file of application """
import random
import logging
import logging_loki
from logging_loki import emitter
from fastapi import FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator
from src.utils import delay_request
from src.config import config

emitter.LokiEmitter.level_tag = "level"

app = FastAPI()
Instrumentator().instrument(app).expose(app)

handler = logging_loki.LokiHandler(
    url=f"{config.loki_instance_uri}/loki/api/v1/push",
    tags={"application": "chatURI"},
    version="1",
)
logger = logging.getLogger("my-logger")
logger.addHandler(handler)


@app.get("/")
async def root():
    """
    The `root` function in Python returns a dictionary with a "message" key set to "Hello World".
    """
    return {"message": "Hello World"}


@app.get("/slow/")
async def slow():
    """
    The `slow` function in Python randomly generates a number and either raises an HTTP 500 error,
    sleeps for 5 seconds before returning a response, or returns a response immediately.
    """
    generated_num = random.randint(1, 3)
    if generated_num == 1:
        logger.error(
            "Internal server error", 
            extra={"tags": {"service": "my-service"}},
        )
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")
    elif generated_num == 2:
        await delay_request.action()
        logger.warning(
            "Slow response", 
            extra={"tags": {"service": "my-service"}},
        )
        return {"message": "slow route response"}
    else:
        pass
    return {"message": "fast response"}
