from src.broker import PikaAioAsyncConsumer
from ...domain import InvokeClientAgentQueueConfig
from ...application import InvokeClientAgentHandler



class PikaAioInvokeClientAgentConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: InvokeClientAgentQueueConfig, 
        handler: InvokeClientAgentHandler
    ):
        super().__init__(config, handler)