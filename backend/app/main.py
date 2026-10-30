import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.config import settings
from backend.app.api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-Grade Multi-Agent Compliance & RFP Due Diligence Engine with LangGraph and RAG"
)

# Enable CORS for Next.js / React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount Frontend Static Assets
frontend_static_dir = os.path.join(settings.BASE_DIR, "frontend", "static")
if os.path.exists(frontend_static_dir):
    app.mount("/static", StaticFiles(directory=frontend_static_dir), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(frontend_static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "message": "Enterprise Compliance Agent Pod API is operational.",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
