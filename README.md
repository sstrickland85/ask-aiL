# RAG Application

A Python application that implements Retrieval-Augmented Generation (RAG) using Ragie for document chunking/vectorizing and an external LLM API for response generation.

## Features

- Generate responses using an LLM based on document context
- View relevant chunks used to contextualize LLM response

## Prerequisites
- Python 3.8 or higher
- Ragie.ai API key
- OpenAI API key

### Step 1: Set Up Your Environment

Create a directory for the project and set up a virtual environment:

#### For macOS/Linux:
```bash
# Create a project directory
mkdir rag-project
cd rag-project

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

#### For Windows:
```bash
# Create a project directory
mkdir rag-project
cd rag-project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/rag-application.git .
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

With your virtual environment activated, run the application:

```bash
python main.py
```

## Basic Commands

- Type your questions at the prompt to get answers from your documents
- Type `help` to see available commands
- Type `exit` to quit the application

## Project Structure

- `main.py`: Entry point for the application
- `config.py`: Configuration and environment variables
- `rag/`: Main application package
  - `clients/`: API client implementations
  - `app.py`: Core RAG application logic
- `.env.example`: Example environment variable file
- `requirements.txt`: Required Python packages

## Future Enhancements

- Web interface using Flask/FastAPI
- Document management features
- Support for local LLM implementations

## Troubleshooting

- **ImportError or ModuleNotFoundError**: Make sure your virtual environment is activated and all dependencies are installed
- **API Key Errors**: Verify that your `.env` file exists and contains valid API keys
- **URL Errors**: If you encounter endpoint errors, check with the API provider for the correct URLs
