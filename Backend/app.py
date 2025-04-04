import os
import re
import shutil
from pathlib import Path
from fastapi import FastAPI,File,UploadFile,HTTPException
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware

from Source.dataIngestion import create_vector_database
from Source.rag import chatbot
from Source.mcq import generate_mcq

PROJECT_HOME_PATH = Path(__file__).resolve().parent



app=FastAPI()


#cors 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR="Data"
os.makedirs(UPLOAD_DIR,exist_ok=True)

class ChatRequest(BaseModel):
    message: str
    filename: str

class McqRequest(BaseModel):
    collection_name:str


def sanitize_filename(filename):
    # Remove all non-word characters (excluding underscores)
    filename = re.sub(r'[^\w\s]', '', filename)
    # Remove all whitespace characters
    filename = re.sub(r'\s+', '', filename)
    return filename


@app.post("/upload/")
async def upload_pdf(file:UploadFile=File(...)):

    #Ensure the uploaded file is a pdf 
    if file.content_type!="application/pdf":
        raise HTTPException(status_code=400,detail="File is not a pdf")
    
    file_location=os.path.join(PROJECT_HOME_PATH,UPLOAD_DIR,file.filename)


    with open(file_location,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    collection_name=sanitize_filename(file.filename)
    create_vector_database(file_location,collection_name)
    
    return {"filename":file.filename,"message":"File uploaded successfully"}


@app.post('/chat')
def chat(request: ChatRequest):
    answer = chatbot(request.message, request.filename)
    return {"response": answer}



@app.post('/mcq')
def mcq(request: McqRequest):
    mcqs=generate_mcq(request.collection_name)

    return {"mcqs":mcqs}