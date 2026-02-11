from fastapi import APIRouter, Depends, Body
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.broker.domain import base_event, producer
from src.broker.infrastructure.pika.producer import RabbitMqProducer
from src.features.knowledge_base.domain import schemas

router = APIRouter(
    prefix="/knowledge-base",
    dependencies=[Depends(verify_hmac)]
)

def get_producer():
    return RabbitMqProducer(
        exchange="documents"
    )

@router.delete("/", status_code=202)
def delete_embeddings(
    data: schemas.DeleteEmbeddingsRequest = Body(...),
    producer: producer.Producer = Depends(get_producer)
):
    pass