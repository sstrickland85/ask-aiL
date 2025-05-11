from fastapi import FastAPI, HTTPException, Request, Form, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import uvicorn
from typing import List, Dict, Any, Optional

# Import RAG components
import config
from rag.clients import RagieClient, OpenAIClient
from rag import RAGApplication
from rag.utils.logging_utils import RagLogger

# Create directories
os.makedirs("templates", exist_ok=True)

# FastAPI app
app = FastAPI(title="RAG Web Interface")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Set up templates
templates = Jinja2Templates(directory="templates")

# Initialize logger
logger = RagLogger()


# Initialize RAG application
def initialize_rag():
    """Initialize RAG clients and application."""
    if not config.RAGIE_API_KEY or not config.LLM_API_KEY:
        raise ValueError("Missing required API keys in configuration")

    ragie_client = RagieClient(
        api_key=config.RAGIE_API_KEY,
        url=config.RAGIE_BASE_URL
    )

    llm_client = OpenAIClient(
        api_key=config.LLM_API_KEY,
        url=config.LLM_API_URL,
        model=config.LLM_MODEL
    )

    return RAGApplication(
        ragie_client=ragie_client,
        openai_client=llm_client
    )


try:
    rag_app = initialize_rag()
except ValueError as e:
    print(f"Failed to initialize RAG application: {str(e)}")
    rag_app = None


# Define API models with validation
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(3, ge=1, le=10)


class QueryResponse(BaseModel):
    response: str
    chunks: List[Dict[str, Any]]


# Define default API key (in production, use a more secure method)
API_ACCESS_KEY = os.environ.get("API_ACCESS_KEY", "default_api_key")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Render the home page with chat interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/query", response_model=QueryResponse)
async def query_endpoint(query_request: QueryRequest, api_key: Optional[str] = Header(None)):
    """API endpoint to query the RAG application."""
    # Check for valid API key
    if api_key != API_ACCESS_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    if not rag_app:
        raise HTTPException(status_code=503, detail="RAG application not initialized")

    try:
        result = rag_app.query(
            query=query_request.query,
            top_k=query_request.top_k
        )
        return result
    except Exception as e:
        # Log the actual error but don't expose details externally
        print(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred processing your request")


@app.post("/chat", response_class=HTMLResponse)
async def chat_form(request: Request, query: str = Form(...)):
    """Handle form submission from the web interface."""
    # Input validation
    if len(query) > 1000:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query[:1000] + "...",
                "error": "Query length exceeds maximum allowed (1000 characters)"
            }
        )

    if not rag_app:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "RAG application not initialized. Check API keys."
            }
        )

    # Use a safer top_k value
    top_k = 3

    try:
        result = rag_app.query(query=query, top_k=top_k)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "response": result["response"],
                "chunks": result["chunks"]
            }
        )
    except Exception as e:
        # Log the actual error but don't expose details to user
        print(f"Chat form error: {str(e)}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "error": "An error occurred while processing your request."
            }
        )


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# For local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)