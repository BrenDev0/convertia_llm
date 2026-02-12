from uuid import UUID
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.features.document_processing.interface.fastapi import routes as document_routes, ws as document_ws
from src.features.embeddings.interface.fastapi import routes as embeddings_routes, ws as embeddings_ws
from src.features.websocket.container import WebsocketConnectionsContainer

def create_fastapi_server():  
    app = FastAPI()

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
    

    app.include_router(document_routes.router)
    app.include_router(document_ws.router)
    app.include_router(embeddings_routes.router)
    app.include_router(embeddings_ws.router)



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