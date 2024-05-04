from pydantic import BaseModel

class module(BaseModel):
    name: str
    description: str
    credits: float
    department_id: int