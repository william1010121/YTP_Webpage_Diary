from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from backend.models import ListRequest
from backend.dependencies import getJsonData

router = APIRouter()

@router.post("/list")
async def list_files(data: ListRequest):
    user_directory = f"./UserData/{data.user}"
    
    # Check if user directory exists
    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail="User directory not found")

    file_list = []
    
    # Iterate through files and get content
    for filename in os.listdir(user_directory):
        file_path = os.path.join(user_directory, filename)
        file_json = getJsonData(file_path)

        file_list.append({"filename": filename.replace(".diary", ""), "content": file_json["Data"], "length": file_json["length"]}) 
    
    return {"file-length": len(file_list), "files": file_list}
