from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.di.container import Container
from src.features.embeddings.domain import schemas
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.persistence.domain.vector_repository import VectorRepository


router = APIRouter(
    prefix="/embeddings",
    dependencies=[Depends(verify_hmac)]
)

def get_vector_repository():
    return Container.resolve("vector_repository")

@router.delete("/", status_code=200)
def delete_embeddings(
    data: schemas.DeleteEmbeddingsRequest = Body(...),
    vector_repository: VectorRepository = Depends(get_vector_repository)
):
    vector_repository.delete_embeddings(
        key=data.key,
        value=data.value
    )

    return JSONResponse(
        status_code=200,
        content="Embeddings deleted"
    )