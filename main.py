from fastapi import FastAPI
from services.ai_workflow import call_workflow

app = FastAPI()

@app.get('/{topic}')
async def find_and_post(topic:str):
  try:
    response = await call_workflow(topic=topic)
    return response
  except Exception as err: 
    return err