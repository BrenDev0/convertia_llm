from src.di import Injector
from .domain import BroadcastingConsumer, BroadcastingQueueConfig
from .infrastructure import PikaAioBroadcastingConsumer
from .application import BroadcastHandler

def register_broker_dependencies(injector: Injector):
    pass

def register_api_dependencies(injector: Injector):
    injector.register(BroadcastHandler)
    injector.register(BroadcastingQueueConfig)
    injector.register(BroadcastingConsumer, PikaAioBroadcastingConsumer)

def register_shared_dependencies(injector: Injector):
    pass