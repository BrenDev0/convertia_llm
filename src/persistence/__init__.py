"""
Stucture:
domain: Abstacts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
interface: access point
di: di registry
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "persistence package for app"


from .domain import (
    DocumentChunk,
    VectorRepository,
    SessionRepository
)

__all__ = [
    #### Domain ####
    "DocumentChunk",
    "VectorRepository",
    "SessionRepository"
]