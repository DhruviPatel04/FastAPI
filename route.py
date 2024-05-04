from ast import main
from asyncio import Server
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Body
from numpy import tri
from pydantic import BaseModel
from pymongo import MongoClient
from models.assessment_info import assessment
from models.feedback_info import feedback
from models.material_info import material
from models.module_info import module
from schema.schemas import list_serial_module, list_serial_student, list_serial_assessment, list_serial_feedback, list_serial_material
from models.student_info import student
from config.database import db
from config.database import collection_name
from config.database import cmodule
from config.database import cassessment
from config.database import cmaterial
from config.database import cfeedback
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import bcrypt


router = APIRouter()



security = HTTPBasic()






#Nsignup

@router.post("/students/")
async def create_student(student: student):
    result = collection_name.insert_one(student.dict())
    return {"message": "Student created successfully", "id": str(result.inserted_id)}

# Route for retrieving information about existing students

@router.get("/students/{student_id}", tags=["student"])
async def student_id():
    students = list_serial_student(collection_name.find())
    return students
   


#  Route to authenticate user(Nlogin)
security = HTTPBasic()

@router.post("/login", tags=["authentication"])
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    # Check if username exists in the database
    existing_student = collection_name.find_one({"username": credentials.username, "password": credentials.password})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    # Check if password matches
    stored_hashed_password = existing_student.get('password')
    if not stored_hashed_password or not bcrypt.checkpw(credentials.password.encode('utf-8'), stored_hashed_password.encode('utf-8')): # type: ignore
        raise HTTPException(status_code=404, detail="Invalid credentials")

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
    return 'success'



#Material

@router.get("/material/{module_id}", tags=["material"])
async def module_id(id):
    material = list_serial_material(cmaterial.find())
    return material

@router.post("/material/insert", tags=["material"])
async def insert_material(material: material = Body(default=None)):
    # Check if email already exists in the database
    existing_material = cmaterial.find_one({"title": material.title})
    if existing_material:
        raise HTTPException(status_code=400, detail="Email already exists")
     
    # Insert student into MongoDB collection
    cmaterial.insert_one(material.dict())
    return 'success'


#ASSESMENT

@router.get("/assessment/{module_id}", tags=["assessment"])
async def module_id(id):
    assessment = list_serial_assessment(cassessment.find())
    return assessment

@router.post("/assessment/insert", tags=["assessment"])
async def insert_assessment(assessment: assessment = Body(default=None)):
    # Check if email already exists in the database
    existing_assessment = cassessment.find_one({"title": assessment.title})
    if existing_assessment:
        raise HTTPException(status_code=400, detail="sucess")
     
    # Insert student into MongoDB collection
    cassessment.insert_one(assessment.dict())
    return 'success'



#FEEDBACK


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


