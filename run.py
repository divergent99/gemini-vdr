"""
run.py — single process: FastAPI + Dash mounted together

Usage:
    python run.py
"""
import uvicorn

if __name__ == "__main__":
    print()
    print("  \033[36m╔══════════════════════════════════════╗\033[0m")
    print("  \033[36m║     VDR VOICE INTELLIGENCE           ║\033[0m")
    print("  \033[36m║     Gemini Live Agent Challenge 2026  ║\033[0m")
    print("  \033[36m╚══════════════════════════════════════╝\033[0m")
    print()
    print("  App → http://localhost:8052")
    print()
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8052, reload=False)
