#!/usr/bin/env python3
import sys
import time
import config
from rag.clients import RagieClient, OpenAIClient
from rag import RAGApplication


def check_configuration():
    """Checks for required API keys"""
    missing = []

    if not config.RAGIE_API_KEY:
        missing.append('RAGIE_API_KEY')

    if not config.LLM_API_KEY:
        missing.append('LLM_API_KEY')

    if missing:
        print("Missing API keys: {}".format(", ".join(missing)))
        return False

    return True


def print_response_with_formatting(response):
    """Prints the response with clean formatting"""
    print("\n" + "=" * 50)
    print("RESPONSE:")
    print("-" * 50)
    print(response)
    print("=" * 50)


def print_chunks(chunks):
    """Prints chunks with formatting"""
    print("\nRETRIEVED CHUNKS:")
    print("-" * 50)
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1} (Score: {chunk.get('score', 'N/A')}):")
        print("-" * 40)
        print(chunk.get("text", "No text available"))
        print("-" * 40)


def main():
    """Entry point for RAG application"""
    if not check_configuration():
        sys.exit(1)

    # Initialize clients
    ragie_client = RagieClient(
        api_key=config.RAGIE_API_KEY,
        url=config.RAGIE_BASE_URL
    )

    llm_client = OpenAIClient(
        api_key=config.LLM_API_KEY,
        url=config.LLM_API_URL,
        model=config.LLM_MODEL
    )

    # Initialize RAG application
    app = RAGApplication(
        ragie_client=ragie_client,
        openai_client=llm_client,
    )

    # Display welcome message
    print("\n==== RAG Application ====")
    print("Type 'exit' to quit the application")
    print("Type 'help' for additional commands")
    print("========================")

    while True:
        query = input("\nAsk aiLeaders chat a question: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if query.lower() == "help":
            print("\nAvailable commands:")
            print("  exit - Exit the application")
            print("  help - Display this help message")
            print("  <query> - Ask a question to search for information")
            continue

        if not query:
            print("Please enter a question.")
            continue

        try:
            print(f"\nProcessing query: '{query}'")
            start_time = time.time()

            # Default to 3 chunks but allow configuration later
            top_k = 3
            result = app.query(query, top_k=top_k)

            # Print performance info
            elapsed = time.time() - start_time
            print(f"Query processed in {elapsed:.2f} seconds")

            # Print the response
            print_response_with_formatting(result["response"])

            # Optionally show chunks
            show_chunks = input("Show retrieved chunks? [y/n] ").strip().lower()
            if show_chunks == "y":
                print_chunks(result["chunks"])

        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or check your API keys.")


if __name__ == "__main__":
    main()