from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from backend.models import UploadRequest
from backend.dependencies import getJsonData, writeJsonData

router = APIRouter()

@router.post("/url")
async def upload_url(data: UploadRequest):
    user_directory = f"./UserData/{data.user}"
    
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    
    current_date = datetime.now().strftime("%m-%d")
    file_path = os.path.join(user_directory, f"{current_date}.diary")
    
    json_data = getJsonData(file_path)
    json_data["Data"].append({
        "id": json_data["length"],
        "type": "url",
        "position": data.url,
        "title": data.title,
        "content": data.content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    json_data["length"] += 1
    writeJsonData(file_path, json_data)
    
    return {"message": f"URL added to {current_date}.diary"}