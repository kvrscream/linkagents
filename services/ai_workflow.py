from llama_index.llms.ollama import Ollama
from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.core.tools import FunctionTool
from services.requests import call_arxiv, build_request
from dotenv import dotenv_values


config = dotenv_values(".env")


# llm = Ollama(model='llama3.2:1b', request_timeout=120.0)
llm = Groq(model=config['MODEL'], api_key=config['APIKEY'])

arxiv_tool = FunctionTool.from_defaults(
  fn=call_arxiv,
  name="BuscarArtigosArxiv",
  description="Busca artigos no arXiv dados uma palavra-chave. Útil para encontrar artigos científicos.")

news_tools = FunctionTool.from_defaults(
  fn=build_request,
  name="BuscaAPINews",
  description="Busca matérias mais recentes da api da new com o topic enviado."
)

agente_resume = FunctionAgent(
  name="AgenteResume",
  description="""Este agente é responsável por formatar o artigo para postar em uma 
    rede social contendo dados como data, link e autor. Além retornar em um formato JSON""",
  llm=llm,
  tools=[],
  streaming=False,
  state_prompt="""Você é deve resumir e editar o texto enviado citar data, link e autor, deixar em um formato 
    agradável para redes sociais e retornar no formato JSON""",
  can_handoff_to=["AgenteBuscador"]
)

agente_busca = FunctionAgent(
  name="AgenteBuscador",
  description="Este agente é responsável por buscar o conteúdo referente ao tópico enviado na internet.",
  llm=llm,
  streaming=False,
  tools=[news_tools], #podemos criar functions customeizadas e passar aqui como novas ferramentas
  system_prompt="""
    Você deve pesquisar usando as tools para encontrar artigos referente ao tópico selecionado! 
    Passeo o conteúdo para o outro agente para deixar bem formatado!
  """,
  can_handoff_to=["AgenteResume"] #Pode chamar outros agentes aqui
)

async def call_workflow(topic:str):
  agent_workflow = AgentWorkflow(
    agents=[agente_busca, agente_resume],
    root_agent=agente_busca.name,
    verbose=True
  )

  resp = await agent_workflow.run(user_msg=topic)
  return resp