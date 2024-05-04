from fastapi import FastAPI
from routes.route import router
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from routes.route import router

app = FastAPI()

app.include_router(router)



# uri = "mongodb+srv://admin:test1234@cluster0.hzeewn2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# #Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

#Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)