from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from datetime import datetime
import json
from typing import Optional
from backend.routers import upload, edit, list, summary, create

app = FastAPI()

# In your FastAPI application
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/uploads", tags=["uploads"])
app.include_router(edit.router, prefix="/api/edit", tags=["edit"])
app.include_router(list.router, prefix="/api", tags=["list"])
app.include_router(summary.router, prefix="/api/summary", tags=["summary"])
app.include_router(create.router, prefix="/api/import", tags=["import"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
# API 2: /api/list


# write openapi schema to file
with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)

