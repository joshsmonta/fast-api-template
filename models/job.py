import uuid
from pydantic import BaseModel, Field

class Job(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    tokens: list[str]
    hasEnded: bool
            
class JobCreateRequest(BaseModel):
    tokens: list[str]
    
class JobPopRequest(BaseModel):
    job_id: str
    token: str
    
    