from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from backend.models import SummaryRequest 
from backend.dependencies import getJsonData, writeJsonData
from backend.tool.summaryAI import summaryJson
from json import dumps

router = APIRouter()

def add_summary_directory(user_directory):
    summary_directory = f"{user_directory}/summary"
    if not os.path.exists(summary_directory):
        os.makedirs(summary_directory)
    return summary_directory

@router.post("/summarize")
async def summaryURL(data: SummaryRequest):
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
    if json_data["Data"] is None or json_data["length"] is None :
        raise HTTPException(status_code=404, detail=f"No data found for the given date")
    summary_directory = add_summary_directory(user_directory)
    summary_path = os.path.join(summary_directory, f"{data.date}.summary")
    summary = summaryJson(dumps(json_data))
    print(type(summary))
    writeJsonData(summary_path, summary)

    return {"message": f"{data.date}.diary summary", "summary": summary}

@router.post("/get_summary")
async def get_summary(data: SummaryRequest):
    user_directory = f"./UserData/{data.user}"
    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail="User directory not found")
    
    # date format is "%m-%d", check the data.date is in this format
    try:
        datetime.strptime(data.date, "%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    summary_directory = f"{user_directory}/summary"
    summary_path = os.path.join(summary_directory, f"{data.date}.summary")
    if not os.path.exists(summary_directory) or not os.path.exists(summary_path):
        return {"message": "No summary found", "summary": { "response": ""}, "metadata": {}}
    summary = getJsonData(summary_path)
    return {"message": f"{data.date}.summary", "summary": summary}