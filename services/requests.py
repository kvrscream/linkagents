import arxiv
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

def call_arxiv(topic: str) -> str:
  search = arxiv.Search(
    query=topic,
    max_results=1,
    sort_by=arxiv.SortCriterion.SubmittedDate
  )
  
  results = list(search.results())

  if not results:
    return "Nenhum artigo encontrado"
  
  formatted = ""
  for i,r in enumerate(results):
    formatted += f"Artigo {i+1}:\n"
    formatted += f"Título: {r.title}\n"
    formatted += f"Autores: {', '.join(a.name for a in r.authors)}\n"
    formatted += f"Publicado em: {r.published.strftime('%Y-%m-%d')}\n"
    formatted += f"Resumo: {r.summary.strip()}\n"
    formatted += f"Link: {r.entry_id}\n\n"

  return formatted.strip()

def build_request(topic:str):
  token = config["NEWSAPIKEY"]
  url = f"{config["NEWSURL"]}{topic}&apiKey={token}&pageSize=1"

  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.get(url,headers=headers)
  print(response)
  return response.json()["articles"][0] if response.status_code == 200 else response.text
