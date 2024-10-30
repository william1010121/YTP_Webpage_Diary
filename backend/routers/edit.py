from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from backend.models import EditRequest
from backend.dependencies import getJsonData, writeJsonData

router = APIRouter()

@router.post("/url")
async def edit_url(data: EditRequest):
    user_directory = f"./UserData/{data.user}"
    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail="User directory not found")
    
    # date format is "%m-%d", check the data.date is in this format
    try:
        datetime.strptime(data.date, "%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    file_path = os.path.join(user_directory, f"{data.date}.diary")
    json_data = getJsonData(file_path)
    if json_data["Data"] is None or json_data["length"] is None or json_data["length"] <= data.index:
        raise HTTPException(status_code=404, detail=f"No data found for the given date")

    if json_data["Data"][data.index]["type"] != "url":
        raise HTTPException(status_code=400, detail="Index does not point to a URL")
    
    json_data["Data"][data.index]["content"] = data.content
    writeJsonData(file_path, json_data)

    return {"message": f"URL at index {data.index} edited in {data.date}.diary", "json_data": json_data}


