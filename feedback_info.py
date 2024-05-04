from pydantic import BaseModel

class feedback(BaseModel):
    student_id: int
    assessment_id: int
    grade: int
    comments: str
 