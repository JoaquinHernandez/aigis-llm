from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import triage

app = FastAPI(title="AegisLLM API", version="1.0.0")

# Restrict CORS to the local Vite dev server and production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage.router)

@app.get("/health")
def health_check():
    return {"status": "AegisLLM Core is operational."}
