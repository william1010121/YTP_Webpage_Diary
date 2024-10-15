from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from datetime import datetime
import json

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

def get_json_data(file_path):
    if not os.path.exists(file_path):
        return {"Data": [], "length": 0}
    with open(file_path) as f:
        data = json.load(f)
    return data
def write_json_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# API 1: /api/uploads
@app.post("/api/uploads/url")
async def upload_url(data: UploadRequest):
    print(data)
    user_directory = f"./UserData/{data.user}"
    
    # Check if user directory exists, if not create it
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    
    # Create or append to the file (MM-DD.diary)
    current_date = datetime.now().strftime("%m-%d")
    file_path = os.path.join(user_directory, f"{current_date}.diary")
    

    json_data = get_json_data(file_path)
    if json_data["Data"] is None:
        json_data["Data"] = []
    if json_data["length"] is None:
        json_data["length"] = 0

    json_data["Data"].append({
        "type": "url",
        "url": data.url,
        "content": "",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    json_data["length"] += 1
    write_json_data(file_path, json_data)
    
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
        file_json = get_json_data(file_path)

        file_list.append({"filename": filename.replace(".diary", ""), "content": file_json["Data"], "length": file_json["length"]}) 
    
    return {"file-length": len(file_list), "files": file_list}


