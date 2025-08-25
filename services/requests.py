import arxiv
import requests

def call_arxiv(topic: str):
  seacrh = arxiv.Search(
    query=topic,
    max_results=1,
    sort_by=arxiv.SortCriterion.SubmittedDate
  )

  return seacrh.results[0]
