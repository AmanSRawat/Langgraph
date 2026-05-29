from typing import Annotated, TypedDict, Sequence
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content: str) -> str:
    """Updates the document with the provided content."""
    global document_content
    document_content = content
    return f"Document has been updated successfully! The current content is: \n{document_content}"

@tool 
def save(filename: str) -> str:
    """Save the current document to a text file and finish the process.
       
       Args:
           filename: Name for the text file."""
    global document_content
    
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    try:
        with open(filename, "w") as f:
            f.write(document_content)
        print(f"Document saved successfully as {filename}")
        return f"Document has been saved successfully as {filename}!"
    except Exception as e:
        return f"Failed to save document: {str(e)}"

tools = [update, save]
tool_node = ToolNode(tools)

llm = ChatGroq(model="llama-3.3-70b-versatile").bind_tools(tools)

def agent(state: AgentState) -> AgentState:
    """This function calls the model and generates a response."""
    system_prompt = SystemMessage(
        content=f"""You are Drafter, a helpful writing assistant. You help the user update and modify documents.

- If the user wants to update or modify content, use the 'update' tool with the complete updated content.
- If the user wants to save and finish, you need to use the 'save' tool.
- Make sure to always show the current document state after modifications.

The current document content is: {document_content}"""
    )
    
    # Take user input dynamically inside the loop
    user_input = input("\nWhat would you like to do with the document? ")
    print(f"User: {user_input}")
    user_message = HumanMessage(content=user_input)
    
    # Combine system prompt, conversation history, and new input
    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    
    response = llm.invoke(all_messages)
    
    if response.content:
        print(f"Drafter: {response.content}")
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")
    
    return {"messages": [user_message, response]}

def should_continue(state: AgentState):
    """Determines whether the agent should execute tools or stop."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM made tool calls, route to the 'tools' node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Check if a tool message indicated that it saved successfully
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and 
            "saved" in message.content.lower() and 
            "document" in message.content.lower()):
            return "end"
            
    return "end"

def print_messages(messages):
    """Prints tool execution updates cleanly"""
    if not messages:
        return
    if isinstance(messages[-1], ToolMessage):
        print(f"🛠️ TOOL RESULT: {messages[-1].content}")

# Building the Graph correctly
graph = StateGraph(AgentState)
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")

# The agent decides whether to call tools or end
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

# After tools run, they must loop back to the agent to process the result
graph.add_edge("tools", "agent")

app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")
    print("Drafter: Hello, I am ready to update the document. Please provide the content you want to update or modify.")
    
    state = {"messages": []}
    
    # Running the stream
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()