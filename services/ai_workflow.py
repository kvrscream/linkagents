from llama_index.llms.ollama import Ollama
from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.core.tools import FunctionTool
from services.requests import call_arxiv
from dotenv import dotenv_values


config = dotenv_values(".env")


# llm = Ollama(model='llama3.2:1b', request_timeout=120.0)
llm = Groq(model=config['MODEL'], api_key=config['APIKEY'])

arxiv_tool = FunctionTool.from_defaults(
  fn=call_arxiv,
  name="BuscarArtigosArxiv",
  description="Busca artigos no arXiv dados uma palavra-chave. Útil para encontrar artigos científicos.")

agente_resume = FunctionAgent(
  name="AgenteResume",
  description="Este agente é responsável por formatar o artigo em até mil caracteres para postar em uma rede social e retornar em um formato JSON",
  llm=llm,
  tools=[],
  streaming=False,
  state_prompt="""Você é deve ediitar o texto enviado em até 1000 caracteres sem esquecer de citar o autor, deixar em um formato 
    agradável para redes sociais e retornar no formato JSON o resumo, ano, link e autor do artigo.""",
  can_handoff_to=["AgenteBuscador"]
)

agente_busca = FunctionAgent(
  name="AgenteBuscador",
  description="Este agente é responsável por buscar o conteúdo referente ao tópico enviado na internet.",
  llm=llm,
  streaming=False,
  tools=[arxiv_tool], #podemos criar functions customeizadas e passar aqui como novas ferramentas
  system_prompt="""
    Você deve pesquisar usando as tools para encontrar artigos referente ao tópico selecionado e 
    retornar seu conteúdo, autor e link! Envie para o outro agente para deixar bem formatado!
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