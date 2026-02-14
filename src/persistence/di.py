from src.di.injector import Injector
from src.persistence.domain import session_repository, vector_repository
from src.persistence.infrastructure.qdrant.vector_repository import QdrantVectorRepository
from src.persistence.infrastructure.redis.session_repository import RedisSessionRepository



def register_shared_dependencies(injector: Injector):
    injector.register(session_repository.SessionRepository, RedisSessionRepository)
    injector.register(vector_repository.VectorRepository, QdrantVectorRepository)