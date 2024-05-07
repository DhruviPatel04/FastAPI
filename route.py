import mimetypes
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, Body, Response, UploadFile
from gridfs import GridFS
from numpy import outer
from models.module_info import module
from schema.schemas import list_serial_module, list_serial_student
from models.login import Signup
from models.student_info import student
from config.database import db
from config.database import collection_name
from config.database import cmodule
from config.database import cassessment
from config.database import cfeedback
from config.database import login_collection
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from bson import ObjectId
from passlib.context import CryptContext







router = APIRouter()

 

fs = GridFS(db)

security = HTTPBasic()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#Nsignup

@router.post("/students/",tags=["students"])
async def create_student(student: student):
    result = collection_name.insert_one(student.dict())
    result = collection_name.insert_one(student.dict())
    return {"message": "Student registered successfully", "id": str(result.inserted_id)}

@router.get("/students/{student_id}", tags=["students"])
async def student_id(student_id: str):
    students = list_serial_student(collection_name.find())
    return students
   


#Login

@router.post("/signup", tags=["authentication"])
async def signup(user: Signup):
    # Check if username already exists
    existing_user = login_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Store user in the database
    login_collection.insert_one({"username": user.username, "password": hashed_password})

    return {"message": "User signed up successfully"}

@router.post("/login", tags=["authentication"])
async def login(username: str, password: str, credentials: HTTPBasicCredentials = Depends(security)):
    # Check if username exists in the database
    existing_user = login_collection.find_one({"username": username})
    if not existing_user:
        raise HTTPException(status_code=404, detail="Invalid username or password")

    # Check if password matches
    stored_hashed_password = existing_user.get('password')
    if not stored_hashed_password or not pwd_context.verify(password, stored_hashed_password):
        raise HTTPException(status_code=404, detail="Invalid username or password")

    # If both username and password are correct, return success message
    return {"message": "Login successful"}




#MODULE 



@router.get("/modules/{department_id}", tags=["module"])
async def department_id(id):
    module = list_serial_module(cmodule.find())
    return module


@router.post("/modules/insert", tags=["module"])
async def insert_module(module: module = Body(default=None)):
    # Check if email already exists in the database
    existing_module = cmodule.find_one({"name": module.name})
    if existing_module:
        raise HTTPException(status_code=400, detail="Already exists")
     
    # Insert student into MongoDB collection
    cmodule.insert_one(module.dict())
    return 'Module instered Successfully'



#Material for the downloading file 

@router.get("/download-teaching-material/{study_material_id}",  tags=["Teaching Material"])
async def download_study_material(study_material_id: str):
    
    try:
        # Verify if class exists
        
        # Verify if study material exists and belongs to the specified class
        study_material = cassessment.find_one({"_id": ObjectId(study_material_id)})
        if study_material is None:
            raise HTTPException(status_code=404, detail="Study material not found for this class")

        # Retrieve file from GridFS using the file ID stored in the study material
        file_info = fs.get(ObjectId(study_material["file_id"]))
        if file_info is None:
            raise HTTPException(status_code=404, detail="File not found")

        # Determine media type based on file extension
        filename = file_info.filename
        media_type, _ = mimetypes.guess_type(filename)
        if media_type is None:
            media_type = "application/octet-stream"

        # Read file content into memory
        file_content = file_info.read()

        # Return file content as response
        return Response(content=file_content, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={filename}"})
    except HTTPException:
        # Re-raise HTTPException to return specific error responses
        raise
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail="Failed to download study material")


#ASSESMENT For UploadFile

@router.post("/upload-excercise/",  tags=["Assignement"])
async def upload_excercise_and_assignment(student_Id:str, class_id:str, excercise_Id:str, topic_name: str,  
                                          assignmentFile: UploadFile = File(...), 
     ):
    # Save file to GridFS
    print(assignmentFile.content_type)
    if assignmentFile.content_type in ('application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg'):
        print('insdf')
        file_id = fs.put(assignmentFile.file, filename=assignmentFile.filename)
    else:
        # sent unsupported media type error
        raise HTTPException(status_code=415, detail='File formate is not supported. Please use PDF,DOC and png formate only') 
    
    # Save metadata to MongoDB
    dataToSave = {
    'student_Id': student_Id,
    'topic_name': topic_name,
    'excercise_Id': excercise_Id,
    "class_id": class_id,
    "file_id": str(file_id),
     }
    # Insert metadata into study_materials collection
    cassessment.insert_one(dataToSave)
    
    return {"message": "File uploaded successfully"}




# FEEDBACK


@router.get("/feedbacks/", tags=["feedback"])
async def get_feedbacks():
    try:
        feedbacks = list(cfeedback.find())
        return feedbacks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedbacks/{student_id}", tags=["feedback"])
async def get_feedback(student_id: int):
    try:
        feedback = cfeedback.find_one({"_id": ObjectId(student_id)})
        if feedback:
            return feedback
        else:
            raise HTTPException(status_code=404, detail="Feedback not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
