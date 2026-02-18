"""
Stucture:
domain: Abstacts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
interface: access point
dependencies: Getter methods for singleton classes
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "tracking package for app"


from .application import ProgressTracker
from .domain import ProgressStage

__all__ = [
    #### Domain ####
    "ProgressStage",

    #### Application ####
    "ProgressTracker"
]