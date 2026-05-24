from typing import TypedDict
from langgraph.graph import StateGraph
from IPython.display import display, Image

class AgentState(TypedDict):
    name: str
    age: int
    final: str


def first_node(state:AgentState)->AgentState:
    """This is the first node"""
    state["final"] = f"Hello {state['name']}!"
    
    return state

def second_node(state:AgentState)->AgentState:
    """This is the second node"""
    
    state["final"] = f"{state['final']} You are {state['age']} years old."
    return state

graph = StateGraph(AgentState)

graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.set_finish_point("second")

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))
answer = app.invoke({"name": "Aman", "age": 25})
print(answer["final"])