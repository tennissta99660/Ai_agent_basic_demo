# step1 : setup api keys from groq, openai and tavily
import os
from langchain_core.prompts import ChatPromptTemplate
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 
TAVILY_API_KEY = os.environ.get("TAVILY_API__KEY")
#step2: setup LLM and  tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
search_tool = TavilySearchResults(max_results=2)
#step 3: setup ai agent with search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai  import AIMessage
prompt = ChatPromptTemplate.from_messages([
    ("system", "Act as an AI ChatBot that is smart and friendly"),
    ("placeholder", "{messages}")
])
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model = llm_id)
    tools = [TavilySearchResults(max_results=2)] if allow_search else []
    agent = create_react_agent(
    model = groq_llm,
    tools = tools,
    prompt = prompt
)
    state = {"messages":query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]
    return ai_messages[-1]
