import json
import os
import uuid
from fastapi import FastAPI, Request, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Define the origins that should be allowed to make cross-origin requests
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,           # Allow cookies and credentials
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)
class DataObject(BaseModel):
    # Define the structure of your incoming object here
    data: Dict[str, Any]
    # ... other fields

@app.post("/save_object")
async def save_object(data: DataObject):
    file_name = f"{uuid.uuid4()}.json"  # Generate a unique filename
    file_path = f"./data/{file_name}"

    os.makedirs("data", exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data.dict(), f, indent=4)

    return {"message": f"Object saved as {file_name}"}

@app.get("/get_object/{file_name}")
async def get_object(file_name: str):
    file_path = f"./data/{file_name}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r") as f:
        data = json.load(f)

    return data


@app.get("/test")
async def get_object():
    return {"field1" : "testing successful"}
