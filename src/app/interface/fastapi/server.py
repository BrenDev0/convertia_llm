from contextlib import asynccontextmanager
from uuid import UUID
from src.di.injector import Injector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.features.document_processing.interface.fastapi import routes as documents_routes
from src.features.embeddings.interface.fastapi import routes as embeddings_routes
from src.features.communication.interface.fastapi import ws as communications_ws
from src.websocket.container import WebsocketConnectionsContainer
from src.app.setup import setup_consumers, setup_dependencies


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("LIFESPAN STARTED")

    api_injector = Injector()

    setup_dependencies(injector=api_injector)
    await setup_consumers(injector=api_injector)

    app.state.injector = api_injector
    yield
   
   

def create_fastapi_server():  
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://localhost:3000", "http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "convertia llm ok"}
    

    app.include_router(documents_routes.router)
    app.include_router(embeddings_routes.router)
    app.include_router(communications_ws.router)



    @app.get("/connections", tags=["Internal"])
    async def get_websocket_connections():
        connections = WebsocketConnectionsContainer._active_connections

        return {
            "connection_ids": list(connections.keys()),
            "count": len(connections)
        }

    @app.delete("/connections/{connection_id}", tags=["Internal"])
    async def get_websocket_connections(
        connection_id: UUID
    ):
        WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)

        connections = WebsocketConnectionsContainer._active_connections

        return {
            "connection_ids": list(connections.keys()),
            "count": len(connections)
        }


    return app