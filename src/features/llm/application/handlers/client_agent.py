from src.broker import AsyncHandler, ChatEvent, CommunicationProducer, ChatsProducer
from src.features.embeddings.application import GetRAGContext
from src.features.messages.application import GetRAGChatHistory
from ...domain import InvokeAgentPayload, LlmService

class InvokeClientAgentHandler(AsyncHandler):
    def __init__(
        self,
        rag_context: GetRAGContext,
        rag_chat_history: GetRAGChatHistory,
        llm_service: LlmService,
        communications_producer: CommunicationProducer,
        chats_producer: ChatsProducer
    ):
        self.__rag_context = rag_context
        self.__rag_chat_history = rag_chat_history
        self.__llm_service = llm_service
        self.__communications_producer = communications_producer
        self.__chats_producer = chats_producer


    async def handle(self, event):
        parsed_event = ChatEvent(**event)
        payload = InvokeAgentPayload(**parsed_event.payload)

        prompt_with_context = await self.__rag_context.execute(
            agent_id=parsed_event.agent_id,
            input=payload.input,
            prompt=payload.prompt
        )

        prompt_with_chat_history = self.__rag_chat_history.execute(
            chat_id=parsed_event.chat_id,
            prompt=prompt_with_context
        )

        chunks = []
        async for chunk in self.__llm_service.interact(prompt=prompt_with_chat_history):
            chunks.append(chunk)
            event_copy = parsed_event.model_copy()
            chunk_payload = {
                "type": "CHUNK",
                "data": str(chunk),
                "transcripts": payload.transcripts
            }

            event_copy.payload = chunk_payload

            ## Send to front end
            await self.__communications_producer.publish(
                routing_key="",
                event= event_copy
            )

        ai_response_payload = {
            "type": "ai",
            "text": " ".join(chunks)
        }

        parsed_event.payload = ai_response_payload
        
        ## update chat history and save message in db
        self.__chats_producer.publish(
            routing_key="chats.history.update",
            event=parsed_event
        )
