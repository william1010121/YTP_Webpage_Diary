from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
import os
import subprocess
import tempfile
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
    json = Markdown2Json(data.markdown)
    returnData = Project.importJson(json)
    if returnData is None or returnData["status"] == "404":
        Project.close()
        return HTTPException(status_code=404, detail=returnData["message"])
    Project.close()
    return {"message": f"Markdown uploaded to {data.projectId}", "Structure": returnData["Structure"]}

def Markdown2Json(markdown) :
    temp = tempfile.NamedTemporaryFile(suffix=".md")
    print(f"Markown: {markdown}")
    with open(temp.name, 'w', encoding='utf-8') as f:
        f.write(markdown)
    cmd = "./backend/tool/bin/md2json"
    subprocess.run([cmd], input=temp.name, text=True)
    with open(temp.name.replace(".md", ".json"), 'r',encoding='utf-8') as f:
        jsonData = json.load(f)
    temp.close()
    #using utf-8 encoding
    print(f"Json: {json.dumps(jsonData, indent=2, ensure_ascii=False)}")
    return jsonData

