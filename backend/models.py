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
class ListProjectRequest(BaseModel):
    user: str
class ProjectRequest(BaseModel) :
    user: str
    projectId: str
class ProjectNodeRequest(BaseModel) :
    user: str
    projectId: str
    nodeId: str
class UploadRequest(BaseModel):
    user: str
    projectId: str
    nodeId: str
    urlType: NodeDataType
    url: str
    title: str
    content: str
class ImportMarkdownRequest(BaseModel):
    user: str
    projectId: str
    markdown: str
class ImportJsonRequest(BaseModel):
    user: str
    projectId: str
    json: dict


class createNodeRequest(BaseModel):
   user: str
   projectId: str
   nodeTitle: Optional[str] = "New Node"

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

class createEdgeRequest(BaseModel) :
    user: str
    projectId: str
    StartNode: str
    EndNode: str
