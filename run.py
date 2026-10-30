"""
AEGIS-OPERATOR: One-Click Enterprise Multi-Agent Pod Launcher
Starts the FastAPI server with LangGraph multi-agent pipeline and serves the React dashboard.
"""
import sys
import os
import io

# Ensure UTF-8 output encoding on all Windows consoles without charmap crash
if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

def main():
    print("=" * 70)
    print("  [AEGIS-OPERATOR] Enterprise Multi-Agent Compliance Engine")
    print("  Orchestrated with LangGraph, Hybrid RAG & OpenTelemetry")
    print("=" * 70)
    print("\n[+] Initializing FastAPI server on port 8000 ...")
    print("[+] Interactive Web Dashboard:     http://localhost:8000")
    print("[+] OpenAPI Swagger Documentation: http://localhost:8000/docs")
    print("\nPress CTRL+C to terminate the pod.\n")

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
