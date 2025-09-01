from fastapi import FastAPI
from services.ai_workflow import call_workflow
from services.requests import call_arxiv, build_request
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
  
@app.get('/test/1')
def find_and_post():
  try:
    response = build_request(topic="Agentes de IA no mercado financeiro")
    return response
  except Exception as err:
    print(err) 
    return err
  