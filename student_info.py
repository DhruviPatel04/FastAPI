from pydantic import BaseModel

class student(BaseModel):
    name: str
    dob: str
    course: str 
    email: str
  
    
    
