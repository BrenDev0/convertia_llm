from src.di import Injector
from .domain import session_repository, vector_repository
from .infrastructure import QdrantVectorRepository, RedisSessionRepository

def register_shared_dependencies(injector: Injector):
    injector.register(session_repository.SessionRepository, RedisSessionRepository)
    injector.register(vector_repository.VectorRepository, QdrantVectorRepository)