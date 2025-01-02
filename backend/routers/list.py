from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from backend.models import ListRequest, ProjectRequest, ListProjectRequest, ProjectNodeRequest
from backend.dependencies import getJsonData
from backend.model.Loader import GraphLoader

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
        if not filename.endswith(".diary"):
            continue
        file_json = getJsonData(file_path)

        file_list.append({"filename": filename.replace(".diary", ""), "content": file_json["Data"], "length": file_json["length"]})
    return {"file-length": len(file_list), "files": file_list}

@router.post("/get_project_list")
async def getProjectList(listProject: ListProjectRequest):
    user_directory = f"./UserData/{listProject.user}/Project"
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    project_list = []
    for project in os.listdir(user_directory):
        if not os.path.isdir(os.path.join(user_directory, project)):
            continue
        project_list.append(project)
    return {"project-length": len(project_list), "projects": project_list}

@router.post("/get_structure")
async def getProjectStructure(project: ProjectRequest):
    user_directory = f"./UserData/{project.user}"
    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail="User directory not found")
    Project = GraphLoader(project.projectId, user_directory)
    return {"structure": Project.getStructure()}


@router.post("/get_nodeconfig")
async def getNodeConfig(project: ProjectRequest):
    user_directory = f"./UserData/{project.user}"
    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail="User directory not found")
    Project = GraphLoader(project.projectId, user_directory)
    return {"nodeconfig": Project.getNodeConfig()}


@router.post("/get_node")
async def getNode(data: ProjectNodeRequest):
    user_directory = f"./UserData/{data.user}"
    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail="User directory not found")
    Project = GraphLoader(data.projectId, user_directory)
    if Project.nodeExists(data.nodeId) == False:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"node": Project.getNode(data.nodeId)}
