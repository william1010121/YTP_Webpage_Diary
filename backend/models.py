from pydantic import BaseModel
from typing import Optional
from enum import Enum


# Define scheemas
class NodeDataType(str,Enum) :
    important = "important"
    relate = "relate"
    other = "other"

    

class Node(BaseModel) :
    ID: str
    children: list[str] # node ID

class Structure(BaseModel) :
    nodes: dict[str, Node] 


# Define request body schemas
class UploadRequest(BaseModel):
    user: str
    nodeId: str
    nodetype: NodeDataType
    url: str
    title: str
    content: str

class EditRequest(BaseModel):
    user: str
    nodeId: str
    date: str
    index: int
    content: Optional[str] = ""
class SummaryRequest(BaseModel):
    user: str
    date: str
class ListRequest(BaseModel):
    user: str

# class SummaryNodeRequest(BaseModel):
#     user: str
#     nodeId: str

# class CreateNodeRequest(BaseModel):
#     user: str
#     projectId: str

# class CreateProjectRequest(BaseModel):
#     user: str
#     projectId: str

class GetProjectStructureRequest(BaseModel):
    user: str
    projectId: str

class UpdateProjectStructureRequest(BaseModel):
    user: str
    projectId: str
    structure: dict[str, Node]

class GetNodeRequest(BaseModel):
    user: str
    nodeId: str    


