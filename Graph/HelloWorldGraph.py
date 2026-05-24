from typing import TypedDict, Dict
from langgraph.graph import StateGraph
from IPython.display import display, Image

class AgentState(TypedDict):
    message: str


def greeting_message(state: AgentState) -> AgentState:
    """Simple function to generate a greeting message."""
    state["message"] = "Hey" + state["message"] + ",how are you doing?"
    
    return state

graph = StateGraph(AgentState)

graph.add_node("greet", greeting_message)

graph.set_entry_point("greet")
graph.set_finish_point("greet")

app = graph.compile()
 
display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"message": "Alice"})

print(result["message"])