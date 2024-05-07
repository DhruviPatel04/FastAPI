from asyncio import Server
from numpy import tri
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:test1234@cluster0.hzeewn2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.student_db

collection_name = db["student_collection"]

cmodule = db["module_collection"]

login_collection = db["login_collection"]

cmaterial = db["material_collection"]

cassessment = db["assessment_collection"]

cfeedback = db["feedback_collection"]


