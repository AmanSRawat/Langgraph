from typing import TypedDict, List
from langgraph.graph import StateGraph
from IPython.display import display, Image
import math

class AgentState(TypedDict):
    num: List[int]
    name: str
    operation: str
    result: str

def perform_operation(state: AgentState) -> AgentState:
    """Simple function to perform an operation on list of numbers."""
    
    if state["operation"] == "*":
        state["result"] = f"Hello {state['name']} the product of the numbers {state['num']} is {math.prod(state['num'])}."
    elif state["operation"] == "+":
        state["result"] = f"Hello {state['name']} the sum of the numbers {state['num']} is {sum(state['num'])}."

    return state
graph = StateGraph(AgentState)

graph.add_node("operate", perform_operation)
graph.set_entry_point("operate")
graph.set_finish_point("operate")

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))
answer = app.invoke({"num": [1, 2, 3, 4], "name": "Aman", "operation": "+"})
answer["result"]