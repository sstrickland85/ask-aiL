from openai import OpenAI
from typing import List


class OpenAIClient:
    """Client for interacting with OpenAI API service."""

    def __init__(self, api_key: str, url: str, model: str):
        self.model = model
        self.url = url
        self.client = OpenAI(api_key=api_key, base_url=url)

    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate a response using the LLM based on query and context."""

        # Format context with clear separators for better responses
        formatted_context = "\n\n---\n\n".join(context)

        # Improved system prompt
        system_prompt = (
            "You are a helpful assistant answering questions based on the provided information. "
            "Use the following context to answer the user's question. "
            "If the answer cannot be found in the context, acknowledge this and provide "
            "the best response you can based on your knowledge. "
            "Keep your answers concise and to the point.\n\n"
            f"CONTEXT:\n{formatted_context}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )

            return completion.choices[0].message.content

        except Exception as e:
            # More informative error message
            error_message = f"OpenAI API error: {str(e)}"
            raise Exception(error_message)