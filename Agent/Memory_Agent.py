from typing import TypedDict, List, Union
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def process(state: AgentState)-> AgentState:
    """This function process the messages and generates a response."""
    response = llm.invoke(state["messages"])
    print("AI: ", response.content)
    state["messages"].append(AIMessage(content=response.content))
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

user_input = input("You: ")
conversation_history = []

with open("conversation_history.txt", "r") as f:    
    for line in f:
        if line.startswith("User: "):
            conversation_history.append(HumanMessage(content=line[len("User: "):].strip()))
        elif line.startswith("AI: "):
            conversation_history.append(AIMessage(content=line[len("AI: "):].strip()))

while user_input!= "exit":
    conversation_history.append(HumanMessage(content=user_input))
    answer = agent.invoke({"messages": conversation_history})
    conversation_history = answer["messages"]
    user_input = input("You: ")
    
with open("conversation_history.txt", "w") as f:
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            f.write("User: " + message.content + "\n")
        else:
            f.write("AI: " + message.content + "\n")
        