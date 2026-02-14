from src.di.injector import Injector
from src.features.communication.domain import consumers
from src.features.communication.infrastructure.pikaaio.consumers import PikaAioBroadcastingConsumer
from src.features.communication.application.handlers import broadcast

def register_broker_dependencies(injector: Injector):
    pass

def register_api_dependencies(injector: Injector):
    injector.register(broadcast.BroadcastHandler)
    injector.register(consumers.BroadcastingQueueConfig)
    injector.register(consumers.BroadcastingConsumer, PikaAioBroadcastingConsumer)

def register_shared_dependencies(injector: Injector):
    pass