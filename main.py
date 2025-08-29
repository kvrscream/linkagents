from fastapi import FastAPI
from services.ai_workflow import call_workflow
from services.requests import call_arxiv
from dotenv import dotenv_values
import os

config = dotenv_values(".env")

app = FastAPI()

@app.get('/{topic}')
async def find_and_post(topic:str):
  try:
    response = await call_workflow(topic=topic)
    return response
  except Exception as err: 
    return err
  
