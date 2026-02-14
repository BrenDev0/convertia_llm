import inspect
from typing import Any

class Injector:
    def __init__(self):
        self._registry = {}
        self._singletons = {}


    def register(self, instance_type, resolve_as=None, *, singleton=True):
        if not resolve_as:
            resolve_as = instance_type

        self._registry[instance_type] = {
            "resolve_as": resolve_as,
            "singleton": singleton
        }


    def resolve(self, instance_type):
        if instance_type in self._singletons:
            return self._singletons[instance_type]
        
        if instance_type not in self._registry:
            raise Exception(f"{instance_type} not registered")
        
        registration = self._registry[instance_type]
        implementation = registration["resolve_as"]
        instance = self._build(implementation)

        if registration["singleton"]:
            self._singletons[instance_type] = instance

        return instance


    def _build(self, cls):
        signature = inspect.signature(cls.__init__)
        dependencies = []

        for name, param in signature.parameters.items():
            if name == "self":
                continue

            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

          
            if param.default is not inspect._empty:
                continue

            dependency_type = param.annotation

            if dependency_type is inspect._empty:
                raise Exception(
                    f"Missing type hint for dependency '{name}' in {cls.__name__}"
                )

            if dependency_type is Any:
                raise Exception(
                    f"Dependency '{name}' in {cls.__name__} is typed as Any"
                )

            dependency_type = param.annotation

            if dependency_type is inspect._empty:
                raise Exception(
                    f"Missing type hint for dependency '{name}' in {cls.__name__}"
                )
        
            dependency = self.resolve(dependency_type)
            dependencies.append(dependency)

        return cls(*dependencies)

        