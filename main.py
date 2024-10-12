from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from datetime import datetime

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



# Define request body schemas
class UploadRequest(BaseModel):
    user: str
    url: str

class ListRequest(BaseModel):
    user: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

# API 1: /api/uploads
@app.post("/api/uploads")
async def upload_url(data: UploadRequest):
    print(data)
    user_directory = f"./UserData/{data.user}"
    
    # Check if user directory exists, if not create it
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    
    # Create or append to the file (MM-DD.diary)
    current_date = datetime.now().strftime("%m-%d")
    file_path = os.path.join(user_directory, f"{current_date}.diary")
    
    with open(file_path, "a") as f:
        f.write(data.url + "\n")
    
    return {"message": f"URL added to {current_date}.diary"}

# API 2: /api/list
@app.post("/api/list")
async def list_files(data: ListRequest):
    user_directory = f"./UserData/{data.user}"
    
    # Check if user directory exists
    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail="User directory not found")

    file_list = []
    
    # Iterate through files and get content
    for filename in os.listdir(user_directory):
        file_path = os.path.join(user_directory, filename)
        with open(file_path, "r") as f:
            content = f.read().strip()
        
        file_list.append({"filename": filename.replace(".diary", ""), "content": content})
    
    return {"file-length": len(file_list), "files": file_list}


