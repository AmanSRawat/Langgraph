from langgraph.graph import StateGraph
from typing import TypedDict, Dict
from IPython.display import display, Image

class AgentState(TypedDict):
    message: str

def greeting_message(state: AgentState) -> AgentState:
    """Simple function to generate a greeting message."""
    state["message"] = "Hello," + state["message"] + " you are doing great work to learn langraph!"
    
    return state

graph = StateGraph(AgentState)

graph.add_node("greet", greeting_message)
graph.set_entry_point("greet")
graph.set_finish_point("greet")

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"message": "Aman"})
result["message"]