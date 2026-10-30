"""
AEGIS-OPERATOR: One-Click Enterprise Multi-Agent Pod Launcher
Starts the FastAPI server with LangGraph multi-agent pipeline and serves the React dashboard.
"""
import sys
import os
import webbrowser

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

def main():
    print("=" * 70)
    print("  🛡️  AEGIS-OPERATOR: Enterprise Multi-Agent Compliance Engine")
    print("  Orchestrated with LangGraph, Hybrid RAG & OpenTelemetry")
    print("=" * 70)
    print("\n[+] Initializing FastAPI server on http://127.0.0.1:8000 ...")
    print("[+] Interactive React & Tailwind Web UI available at: http://127.0.0.1:8000")
    print("[+] OpenAPI Swagger Documentation available at: http://127.0.0.1:8000/docs")
    print("\nPress CTRL+C to terminate the pod.\n")

    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
