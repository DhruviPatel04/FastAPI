from pydantic import BaseModel

class student(BaseModel):
    name: str
    username: str
    dob: str
    email: str
    password: str
    department_id: int
    
    
