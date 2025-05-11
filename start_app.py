#!/usr/bin/env python3
import argparse
import os
import sys
import webbrowser
from threading import Timer

import uvicorn
import config


def check_configuration():
    """Checks for required API keys"""
    missing = []

    if not config.RAGIE_API_KEY:
        missing.append('RAGIE_API_KEY')

    if not config.LLM_API_KEY:
        missing.append('LLM_API_KEY')

    if missing:
        print("Missing API keys: {}".format(", ".join(missing)))
        print("Please set them in your .env file or environment variables")
        return False

    return True


def open_browser(host, port):
    """Open the browser after a short delay"""
    # Create the URL with correct protocol
    url = f"http://{host}:{port}"
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Unable to open browser automatically: {e}")
        print(f"Please manually navigate to: {url}")


def main():
    parser = argparse.ArgumentParser(description="Start the RAG Web Application")
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    parser.add_argument('--host', type=str, default="127.0.0.1", help='Host to run the server on')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    args = parser.parse_args()

    if not check_configuration():
        sys.exit(1)

    # Generate a default API key if not set
    if not os.environ.get("API_ACCESS_KEY"):
        import secrets
        api_key = secrets.token_hex(16)
        os.environ["API_ACCESS_KEY"] = api_key
        print(f"Generated API key for this session: {api_key}")
        print("To make this permanent, set API_ACCESS_KEY in your environment or .env file")

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    print(f"Starting RAG Web Application on http://{args.host}:{args.port}")

    # Open browser after a delay unless --no-browser is specified
    if not args.no_browser:
        Timer(1.5, open_browser, [args.host, args.port]).start()

    try:
        # Start the server
        uvicorn.run("web_app:app", host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()