from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from backend.model.Loader import GraphLoader 
from backend.models import ImportJsonRequest, ImportMarkdownRequest

router = APIRouter()


@router.post("/json")
async def importJson(data: ImportJsonRequest):
    user_directory = f"./UserData/{data.user}"
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    Project = GraphLoader(data.projectId, user_directory)
    returnData = Project.importJson(data.json)
    if returnData is None or returnData["status"] == "404":
        Project.close()
        return HTTPException(status_code=404, detail=returnData["message"])
    Project.close()
    return {"message": f"Json uploaded to {data.projectId}", "Structure": returnData["Structure"]}

@router.post("/markdown")
async def importMarkdown(data: ImportMarkdownRequest) :
    user_directory = f"./UserData/{data.user}"
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    Project = GraphLoader(data.projectId, user_directory)
    returnCode = Project.importMarkdown(data.markdown)
    
    Project.close()
    return {"message": f"Markdown uploaded to {data.projectId}"}
