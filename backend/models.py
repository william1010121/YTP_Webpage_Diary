from pydantic import BaseModel
from typing import Optional
# Define request body schemas
class UploadRequest(BaseModel):
    user: str
    url: str
    title: str
    content: str

class EditRequest(BaseModel):
    user: str
    date: str
    index: int
    content: Optional[str] = ""

class SummaryRequest(BaseModel):
    user: str
    date: str
    type: str
class ListRequest(BaseModel):
    user: str

