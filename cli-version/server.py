#!/usr/bin/env python3
"""
MoneyMind Dashboard Server
Run: python server.py → http://localhost:8000
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import uvicorn

app = FastAPI(title="MoneyMind Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRIPT_DIR    = Path(__file__).parent
DASHBOARD_DIR = Path.home() / "Documents" / "Finances" / "Dashboard"
DATA_FILE     = DASHBOARD_DIR / "dashboard_data.json"
INDEX_FILE    = DASHBOARD_DIR / "index.html"


def ensure_index_html():
    """
    Copy index.html from script directory to Dashboard folder if needed.
    This runs once at server startup so the page is always available.
    """
    if INDEX_FILE.exists():
        return  # Already there

    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    candidates = [
        SCRIPT_DIR / "index.html",
        SCRIPT_DIR / "templates" / "dashboard" / "index.html",
    ]
    for src in candidates:
        if src.exists():
            shutil.copy2(src, INDEX_FILE)
            print(f"   📋 Copied index.html → {INDEX_FILE}")
            return

    # Write a helpful fallback so the user knows what to do
    INDEX_FILE.write_text("""<!DOCTYPE html>
<html>
<head><title>MoneyMind</title>
<style>body{background:#0f172a;color:white;font-family:sans-serif;
padding:40px;text-align:center}</style></head>
<body>
<h1>💎 MoneyMind</h1>
<p style="color:#ef4444">index.html not found next to server.py</p>
<p>Place <strong>index.html</strong> in the same folder as server.py, then restart.</p>
<p><a href="/dashboard_data.json" style="color:#22c55e">View raw data</a></p>
</body></html>""")
    print("   ⚠️  index.html not found — wrote fallback page")


@app.get("/")
def serve_dashboard():
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE, media_type="text/html")
    return HTMLResponse("<h1>index.html missing — restart server after placing index.html next to server.py</h1>", status_code=404)


@app.get("/dashboard_data.json")
def serve_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            return JSONResponse(json.load(f))
    return JSONResponse({"error": "No data yet — run: python moneymind.py organize"}, status_code=404)


@app.post("/refresh")
def refresh_data():
    """Re-run dashboard JSON generator and return fresh data."""
    script = SCRIPT_DIR / "generate_dashboard_json.py"
    if not script.exists():
        return JSONResponse({"status": "error", "detail": "generate_dashboard_json.py not found"}, status_code=500)
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and DATA_FILE.exists():
            with open(DATA_FILE, encoding="utf-8") as f:
                return JSONResponse({"status": "ok", "data": json.load(f)})
        return JSONResponse({"status": "error", "detail": result.stderr[-500:]}, status_code=500)
    except Exception as e:
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=500)


@app.get("/health")
def health():
    return {
        "status": "running",
        "index_html": INDEX_FILE.exists(),
        "data_json": DATA_FILE.exists(),
    }


if __name__ == "__main__":
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    print("\n💎 MoneyMind Dashboard Server")
    print("=" * 40)

    # Auto-copy index.html before starting
    ensure_index_html()

    print(f"   Dashboard: http://localhost:8000")
    print(f"   Data API:  http://localhost:8000/dashboard_data.json")
    print(f"   Refresh:   POST http://localhost:8000/refresh")
    print("=" * 40)
    print("   Press Ctrl+C to stop\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)