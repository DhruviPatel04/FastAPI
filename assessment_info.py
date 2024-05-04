from datetime import datetime
from pydantic import BaseModel

class assessment(BaseModel):
    title: str
    description: str
    deadline: datetime # Assuming using Python's datetime for deadline
    status: str
    module_id: int 



