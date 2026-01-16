from fastapi import FastAPI

def create_fastapi_server():  
    app = FastAPI()

    @app.get("/health", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "convertia llm ok"}

    # @app.get("/connections", tags=["Internal"])
    # async def get_websocket_connections():
    #     connections = WebsocketConnectionsContainer._active_connections

    #     return {
    #         "connection_ids": list(connections.keys()),
    #         "count": len(connections)
    #     }

    # @app.delete("/connections/{connection_id}", tags=["Internal"])
    # async def get_websocket_connections(
    #     connection_id: UUID
    # ):
    #     WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)

    #     connections = WebsocketConnectionsContainer._active_connections

    #     return {
    #         "connection_ids": list(connections.keys()),
    #         "count": len(connections)
    #     }


    # @app.get("/instances", tags=["Internal"])
    # async def instances():
    #     """
    #     ## Gets instances registered in the dependencies ccontainer
    #     """
    #     return Container.get_instances()

    # app.include_router(interactions_ws.router)

    return app