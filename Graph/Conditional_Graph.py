from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image

class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    final: str

def addition(state: AgentState) ->  AgentState:
    """Function to perform addition."""
    
    state["final"] = f"The sum of {state['number1']} and {state['number2']} is {state['number1'] + state['number2']}."
    return state

def subtraction(state: AgentState) ->  AgentState:
    """Function to perform subtraction."""
    
    state["final"] = f"The difference of {state['number1']} and {state['number2']} is {state['number1'] - state['number2']}."
    return state

def decide_next_node(state: AgentState)->AgentState:
    """Router to route to different nodes based on the operation."""
    
    if state["operation"] == "+":
        return "addition_operation"
    elif state["operation"] == "-":
        return "subtraction_operation"
    

graph = StateGraph(AgentState)
graph.add_node("add_node", addition)
graph.add_node("subtract_node", subtraction)
graph.add_node("router", lambda state:state)

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node"
    }
)

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))
answer = app.invoke({"number1": 10, "operation": "-", "number2": 5})
print(answer["final"])
    