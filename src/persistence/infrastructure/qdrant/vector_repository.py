from uuid import UUID
import qdrant_client
from qdrant_client import models
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

    def store_embeddings(self, embeddings, chunks, namespace = "convertia"):
        collection_exists = self._check_namespace_exists(name=namespace)

        if not collection_exists:
            self.create_namespace(name=namespace, size= len(embeddings[0]))

        points = []

        for chunk, embedding in zip(chunks, embeddings):
            points.append(
                models.PointStruct(
                    id=chunk.chunk_id,
                    vector=embedding,
                    payload={
                        **chunk.metadata,
                        "content": chunk.content,
                        
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

        self.__client.create_payload_index(
            collection_name=name,
            field_name="knowledge_id",
            field_schema="keyword"
        )



    def _check_namespace_exists(
        self,
        name: str
    ):
        ## http://api.qdrant.tech/api-reference/collections/collection-exists
        return self.__client.collection_exists(
            collection_name=name
        )

        
    
    def delete_namespace(self, namespace):
        self.__client.delete_collection(collection_name=namespace)

    
    def delete_embeddings(self, key: str, value: UUID, namespace: str = "convertia",):
        self.__client.delete(
            collection_name=namespace,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    ]
                )
            )
        )

    
    

        
    
    
    
    

