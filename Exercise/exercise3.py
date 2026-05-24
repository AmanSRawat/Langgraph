from typing import TypedDict, List
from langgraph.graph import StateGraph
from IPython.display import display, Image

class AgentState(TypedDict):
    name:str
    age: int
    skills: List[str]
    final: str

def first_node(state:AgentState)->AgentState:
    """This is the first node"""
    state["final"] = f"Hello {state['name']}!"
    
    return state

def second_node(state:AgentState)->AgentState:
    """This is the second node"""
    
    state["final"] = f"{state['final']} You are {state['age']} years old."
    return state

def third_node(state:AgentState)->AgentState:
    """This is the third node"""
    
    state["final"] = f"{state['final']} Your skills are {','.join(state['skills'])}."
    return state

graph = StateGraph(AgentState)
graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.add_node("third", third_node)

graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.add_edge("second", "third")
graph.set_finish_point("third")

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))
answer = app.invoke({"name": "Aman", "age": 25, "skills": ["Python", "Machine Learning", "Langgraph"]})
print(answer["final"])