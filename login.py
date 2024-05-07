from pydantic import BaseModel, Field

class Signup(BaseModel):
    username: str 
    password: str 