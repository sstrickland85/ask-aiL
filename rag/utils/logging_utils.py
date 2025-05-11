import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


class RagLogger:
    """Minimalist logger for RAG application that captures input, output, and chunks."""

    def __init__(self, log_dir: str = "logs", max_file_size_mb: int = 10):
        # Store log directory
        self.log_dir = log_dir

        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # Create a unique session ID
        self.session_id = str(uuid.uuid4())

        # Set maximum file size (convert to bytes)
        self.max_file_size = max_file_size_mb * 1024 * 1024

        # Initialize log file
        self._initialize_log_file()

    def _initialize_log_file(self):
        """Create a new log file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"{self.log_dir}/rag_log_{timestamp}.json"

        # Create the initial log structure
        with open(self.log_file, 'w') as f:
            json.dump({
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "queries": []
            }, f)

    def log_interaction(self, query: str, response: str, chunks: List[Dict[str, Any]]) -> None:
        """Log a complete query-response interaction with chunks."""
        # Check if we need to rotate the log file due to size
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_file_size:
            self._initialize_log_file()  # Create a new log file

        # Create record with timestamp
        record = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "chunks": chunks
        }

        try:
            # Read existing log
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)

            # Add new record
            log_data["queries"].append(record)

            # Write updated log
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

            # Print brief confirmation
            print(f"Logged interaction: {query[:50]}{'...' if len(query) > 50 else ''}")

        except Exception as e:
            # Handle any errors during logging without disrupting the main application
            print(f"Error writing to log file: {str(e)}")

            # Try to recover by creating a new log file
            try:
                self._initialize_log_file()
            except Exception:
                print("Failed to create new log file")