import qdrant_client
from qdrant_client import models
from uuid import uuid4
from src.persistence.domain.vector_repository import VectorRepository

class QdrantVectorRepository(VectorRepository):
    def __init__(
        self,
        connection_url: str,
        api_key: str 
    ):
        self.__client = qdrant_client.QdrantClient(
            url=connection_url,
            api_key=api_key
        )

    def store_embeddings(self, embeddings, chunks, namespace, **kwargs):
        collection_exists = self._check_namespace_exists(name=namespace)

        if not collection_exists:
            self.create_namespace(name=namespace, size= len(embedding[0]))

        points = []

        for chunk, embedding in zip(chunks, embeddings):
            points.append(
                models.PointStruct(
                    id=uuid4(),
                    vector=embedding,
                    payload={
                        **chunk.metadata,
                        **kwargs, # Include filename, user_id, agent_id, etc.
                        "conetent": chunk.content,
                        
                    }
                )
            )

        
        batch_size = 64
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            ## https://api.qdrant.tech/api-reference/points/upsert-points
            self.__client.upsert(
                collection_name=namespace,
                points=batch
            )
        

        return 
        
    def create_namespace(
        self,
        name: str,
        size: int
    ):
        ## https://api.qdrant.tech/api-reference/collections/create-collection
        self.__client.create_collection(
            collection_name={name},
            vectors_config=models.VectorParams(
                size=size,
                distance=models.Distance.COSINE
            )
        )

        ## https://api.qdrant.tech/api-reference/indexes/create-field-index
        self.__client.create_payload_index(
            collection_name=name,
            field_name="user_id",
            field_schema="keyword"
        )

        self.__client.create_payload_index(
            collection_name=name,
            field_name="agent_id",
            field_schema="keyword"
        )



    def _check_namespace_exists(
        self,
        name: str
    ):
        ## http://api.qdrant.tech/api-reference/collections/collection-exists
        res = self.__client.collection_exists(
            collection_name=name
        )

        collection_exists = res.result.exists # bool

        return collection_exists
    
    def delete_namespace(self, namespace):
        self.__client.delete_collection(collection_name=namespace)

    
    def delete_user_data(self, user_id):
        user_prefix = f"user_{user_id}_" 
        collections = self.__client.get_collections()

        for collection in collections.collections:
            if collection.name.startswith(user_prefix):
                self.__client.delete_collection(collection.name)

        
        return 

    
    

        
    
    
    
    

