from typing import List, Dict, Any, Optional

from rag.clients import RagieClient, OpenAIClient

class RAGApplication:
    """Main RAG application that retrieves chunks and passes to LLM for response."""

    def __init__(self, ragie_client: RagieClient, openai_client: OpenAIClient) -> None:
        self.ragie_client = ragie_client
        self.openai_client = openai_client

    def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Perform a RAG query operation."""

        chunks = self.ragie_client.retrieve_chunks(query, top_k)
        chunk_text = [chunk["text"] for chunk in chunks]

        #Generate LLM response
        response = self.openai_client.generate_response(query, chunk_text)

        return {
            "chunks": chunks,
            "response": response
        }