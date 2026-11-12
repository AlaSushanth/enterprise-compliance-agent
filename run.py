"""
AEGIS-OPERATOR: One-Click Enterprise Multi-Agent Pod Launcher
Starts the FastAPI server with LangGraph multi-agent pipeline and serves the React dashboard.
"""
import sys
import os
import io
import socket

# Ensure UTF-8 output encoding on all Windows consoles without charmap crash
if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

def find_available_port(preferred_ports=[8080, 8500, 8000, 8888]):
    for port in preferred_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except Exception:
                continue
    return 8080

def main():
    port = find_available_port()
    
    print("=" * 70)
    print("  [AEGIS-OPERATOR] Enterprise Multi-Agent Compliance Engine")
    print("  Orchestrated with LangGraph, Hybrid RAG & OpenTelemetry")
    print("=" * 70)
    print(f"\n[+] Active Port Selected:          {port}")
    print(f"[+] Interactive Web Dashboard:     http://localhost:{port}")
    print(f"[+] OpenAPI Swagger Documentation: http://localhost:{port}/docs")
    print("\nPress CTRL+C to terminate the pod.\n")

    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=port, reload=False)

if __name__ == "__main__":
    main()
