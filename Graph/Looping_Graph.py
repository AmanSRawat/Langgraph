from typing import TypedDict, List
from langgraph.graph import StateGraph, END, START
from IPython.display import display, Image
import random

class AgentState(TypedDict):
    name: str
    numbers: List[int]
    counter: int
    

def greeting_node(state:AgentState) -> AgentState:
    """This is the greeting node."""
    
    state["name"] = "Hello " + state["name"] + "!"
    state["counter"] = 0
    return state

def random_node(state: AgentState)-> AgentState:
    """This is a random node to include the random number in the list"""
    state["numbers"].append(random.randint(0, 10))
    state["counter"] += 1
    return state

def should_continue(state: AgentState)-> AgentState:
    """This node checks if we should continue or not."""
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"
    else:
        return "exit"

graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")
graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop": "random",
        "exit": END
    }
)

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))
answer = app.invoke({"name": "Aman", "numbers": [],"counter": 1})
print(answer)