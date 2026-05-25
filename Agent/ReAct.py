from typing import Annotated, TypedDict, Sequence
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import SystemMessage, BaseMessage, ToolMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
@tool 
def add(a: int, b: int) -> int:
    """This function adds two numbers."""
    print(f"Adding {a} and {b}")
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """This function subtracts two numbers."""
    print(f"Subtracting {b} from {a}")
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """This function multiplies two numbers."""
    print(f"Multiplying {a} and {b}")
    return a * b

tools = [add, subtract,multiply]

llm = ChatGroq(model="llama-3.3-70b-versatile").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    """This function calls the model and generates a response."""
    system_prompt = SystemMessage(
        content = "You are a helpful assistant who answers the user's query to the best of your ability. Use the available tools when needed to compute answers, and provide a final clear answer after using tools."
    )
    response = llm.invoke([system_prompt] + state["messages"])
    print(state["messages"])

    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls: 
        return "tool"
    else:
        return "end"
    

graph = StateGraph(AgentState)
graph.add_node("model_call", model_call)
graph.add_edge(START, "model_call")
tool_node = ToolNode(tools)
graph.add_node("tool_node", tool_node)
graph.add_conditional_edges(
    "model_call",
    should_continue,
    {
        "tool": "tool_node",
        "end": END
    }
)
graph.add_edge("tool_node", "model_call")
agent = graph.compile()

def print_stream(stream):

    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 2 + 3 and multiply the result by 4.")]}
print_stream(agent.stream(inputs, stream_mode="values"))