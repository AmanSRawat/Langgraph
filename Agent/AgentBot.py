from typing import TypedDict, List
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def process(state: AgentState)-> AgentState:
    """This function processes the messages and generates a response."""
    response  = llm.invoke(state["messages"])
    print("AI: ", response.content)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()

user_input = input("You: ")
while user_input != "exit":
    answer = app.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("You: ")