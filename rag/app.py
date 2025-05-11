from typing import List, Dict, Any, Optional

from rag.clients import RagieClient, OpenAIClient
from rag.utils.logging_utils import RagLogger


class RAGApplication:
    """Main RAG application that retrieves chunks and passes to LLM for response."""

    def __init__(self, ragie_client: RagieClient, openai_client: OpenAIClient) -> None:
        """Initialize with clients - matches the original signature."""
        self.ragie_client = ragie_client
        self.openai_client = openai_client
        # Create a default logger internally
        self._logger = RagLogger()

    def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Perform a RAG query operation."""
        # Retrieve chunks from Ragie
        chunks = self.ragie_client.retrieve_chunks(query, top_k)
        chunk_text = [chunk["text"] for chunk in chunks]

        # Generate LLM response
        response = self.openai_client.generate_response(query, chunk_text)

        # Log the interaction
        self._logger.log_interaction(query, response, chunks)

        return {
            "chunks": chunks,
            "response": response
        }