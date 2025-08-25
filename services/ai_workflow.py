from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.core.tools import FunctionTool
from services.requests import call_arxiv

llm = Ollama(model='llama3.2:1b', request_timeout=120.0)

arxiv_tool = FunctionTool.from_defaults(
  fn=call_arxiv,
  name="BuscarArtigosArxiv",
  description="Busca artigos no arXiv dados uma palavra-chave. Útil para encontrar artigos científicos.")

agente_resume = FunctionAgent(
  name="AgenteResume",
  description="Este agente é responsável por resumir o artigo em até mil caracteres e retornar em um formato JSON",
  llm=llm,
  tools=[],
  state_prompt="Você é deve resumir o texto enviado em até 1000 caracteres e retornar no formato JSON o resumo e autor do artigo.",
  can_handoff_to=[]
)

agente_busca = FunctionAgent(
  name="AgenteBuscador",
  description="Este agente é responsável por buscar o conteúdo referente ao tópico enviado na internet.",
  llm=llm,
  tools=[arxiv_tool], #podemos criar functions customeizadas e passar aqui como novas ferramentas
  system_prompt="Você deve pesquisar na rede em busca de artigos regerente ao tópico selecionado e retornar seu conteúdo!",
  can_handoff_to=["agente_resume"] #Pode chamar outros agentes aqui
)

async def call_workflow(topic:str):
  agent_workflow = AgentWorkflow(
    agents=[agente_busca, agente_resume],
    root_agent=agente_busca.name
  )

  resp = await agent_workflow.run(user_msg=f"Busque um artigo na internet refente ao tópico {topic} e me retorne no formato JSON")
  print(resp)
  return resp