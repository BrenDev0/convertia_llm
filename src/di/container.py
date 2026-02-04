from typing import TypeVar, Dict, cast, List, Callable
from src.di.domain.exceptions import DependencyNotRegistered

T = TypeVar('T')
class Container:
    __instances:  Dict[str, T] = {}
    __factories: Dict[str, Callable[[], T]] = {}

    @classmethod
    def register(cls, key: str, instance: T) -> None:
        cls.__instances[key] = instance

    @classmethod
    def register_factory(cls, key: str, factory: Callable[[], T]):
        cls.__factories[key] = factory

    @classmethod
    def resolve(cls, key: str):
        if key in cls.__instances:
            return cls.__instances[key]
        
        if key in cls.__factories:
            instance = cls.__factories[key]()
            cls.__instances[key] = instance
            return cast(T,instance)
        
        raise DependencyNotRegistered(f"Dependency '{key}' not registerd!")
    
    @classmethod
    def clear(cls) -> None:
        cls.__instances.clear()
        cls.__factories.clear()

    @classmethod
    def get_instances(cls) -> List[str]:
        return list(cls.__instances.keys())