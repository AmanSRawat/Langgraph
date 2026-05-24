from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image

class AgentState(TypedDict):
    num1: int
    operation1: str
    num2: int
    num3: int
    operation2: str
    num4: int
    finalAnswer1: int
    finalAnswer2: int

def addition1(state: AgentState) -> AgentState:
    """This node performs addition."""
    state["finalAnswer1"] = state["num1"] + state["num2"]
    return state

def subtraction1(state: AgentState) -> AgentState:
    """This node performs subtraction."""
    state["finalAnswer2"] = state["num3"] - state["num4"]
    return state

def decide_next_operation1(state: AgentState) -> AgentState:
    """This node decides which operation to perform based on the input."""
    if state["operation1"] == "+":
        return "addition_node_1"
    elif state["operation1"] == "-":
        return "subtraction_node_1"

def addition2(state: AgentState)-> AgentState:
    """This node performs addition on the results of the previous operations."""
    state["finalAnswer2"] = state["num3"] + state["num4"]
    return state

def subtraction2(state: AgentState)-> AgentState:
    """This node performs subtraction on the results of the previous operations."""
    state["finalAnswer2"] = state["num3"] - state["num4"]
    return state

def decide_next_operation2(state: AgentState) -> AgentState:
    """This node decides which operation to perform based on the input."""
    if state["operation2"] == "+":
        return "addition_node_2"
    elif state["operation2"] == "-":
        return "subtraction_node_2"

graph = StateGraph(AgentState)
graph.add_node("add_node_1", addition1)
graph.add_node("subtract_node_1", subtraction1)
graph.add_node("router1", lambda state:state)
graph.add_node("add_node_2", addition2)
graph.add_node("subtract_node_2", subtraction2)
graph.add_node("router2", lambda state:state)

graph.add_edge(START, "router1")
graph.add_conditional_edges(
    "router1",
    decide_next_operation1,
    {
        "addition_node_1": "add_node_1",
        "subtraction_node_1": "subtract_node_1"
    }
)

graph.add_edge("add_node_1", "router2")
graph.add_edge("subtract_node_1", "router2")
graph.add_conditional_edges(
    "router2",
    decide_next_operation2,
    {
        "addition_node_2": "add_node_2",
        "subtraction_node_2": "subtract_node_2"
    }
)
graph.add_edge("add_node_2", END)
graph.add_edge("subtract_node_2", END)

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))
answer = app.invoke({
    "num1": 10,
    "operation1": "+",
    "num2": 5,
    "num3": 20,
    "operation2": "-",
    "num4": 8
})

print(f"The result of the first operation is: {answer['finalAnswer1']}")
print(f"The result of the second operation is: {answer['finalAnswer2']}")