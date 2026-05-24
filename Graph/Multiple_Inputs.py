from typing import TypedDict, List
from langgraph.graph import StateGraph
from IPython.display import display, Image

class AgentState(TypedDict):
    num: List[int]
    name: str
    result: int

def add_numbers(state: AgentState) -> AgentState:
    """Simple function to add numbers."""
    
    print(state)
    state["result"] = f"Hello {state['name']}, the sum of {state['num']} is {sum(state['num'])}."
    print(state)
    return state

graph = StateGraph(AgentState)

graph.add_node("add", add_numbers)
graph.set_entry_point("add")
graph.set_finish_point("add")

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))

answer = app.invoke({"num": [1, 2, 3, 4], "name": "Aman"})
print(answer["result"])