from fastapi import APIRouter, Depends, Body, Request
from fastapi.responses import JSONResponse
from src.di.injector import Injector
from src.features.embeddings.domain import schemas
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.persistence.domain.vector_repository import VectorRepository


router = APIRouter(
    prefix="/embeddings",
    dependencies=[Depends(verify_hmac)]
)

def get_injector(request: Request):
    return request.app.state.injector

@router.delete("/", status_code=200)
def delete_embeddings(
    data: schemas.DeleteEmbeddingsRequest = Body(...),
    injector: Injector = Depends(get_injector)
):
    vector_repository = injector.resolve(VectorRepository)
    vector_repository.delete_embeddings(
        key=data.key,
        value=data.value
    )

    return JSONResponse(
        status_code=200,
        content="Embeddings deleted"
    )