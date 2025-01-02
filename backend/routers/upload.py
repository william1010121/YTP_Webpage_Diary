from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from backend.models import UploadRequest, createNodeRequest, createEdgeRequest
from backend.dependencies import getJsonData, writeJsonData
from backend.model.Loader import GraphLoader

router = APIRouter()

@router.post("/url")
async def upload_url(data: UploadRequest):
    user_directory = f"./UserData/{data.user}"
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    Project = GraphLoader(data.projectId, user_directory)
    nodeJson = Project.insertNodeUrl(data.nodeId, data)
   # current_date = datetime.now().strftime("%m-%d")
    # file_path = os.path.join(user_directory, f"{current_date}.diary")
    # json_data = getJsonData(file_path)
    # json_data["Data"].append({
    #     "id": json_data["length"],
    #     "type": "url",
    #     "position": data.url,
    #     "title": data.title,
    #     "content": data.content,
    #     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # })
    # json_data["length"] += 1
    # writeJsonData(file_path, json_data)
    return {"message": f"URL uploaded to {data.projectId}", "node": nodeJson}

@router.post("/create_node")
async def create_node(data: createNodeRequest):
    user_directory = f"./UserData/{data.user}"
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    Project = GraphLoader(data.projectId, user_directory)
    newNodeID = Project.createNode(data.nodeTitle)
    Project.close()
    return {"message": f"Node created with ID {newNodeID}", "ID": newNodeID}

@router.post("/create_edge")
async def create_edge(data: createEdgeRequest):
    user_directory = f"./Userdata/{data.user}"
    if not os.path.exists(user_directory) :
        return {"message": "User directory not found"}
    Project = GraphLoader(data.projectId, user_directory)
    print(Project.nodeExists(data.StartNode), Project.nodeExists(data.EndNode))
    if not Project.nodeExists(data.StartNode) or not Project.nodeExists(data.EndNode):
        return {"message": "Node not found"}
    structConfig = Project.createEdge(data.StartNode, data.EndNode)
    Project.close()
    return {"message": "Edge created", "structure": structConfig}
