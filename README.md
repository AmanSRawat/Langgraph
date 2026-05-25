# AI Agents with LangGraph

This project is a learning repository for building AI agents using the [LangGraph](https://langchain-ai.github.io/langgraph/) framework. It contains various examples, exercises, and implementations to understand and experiment with LangGraph concepts.


## Getting Started

1. Clone the repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env` (if required by specific examples)
4. Run the examples:
   ```bash
   python Agent/ReAct.py
   python Exercise/exercise1.py
   python Graph/HelloWorldGraph.py
   ```

## Learning Objectives

Through this project, you will learn:
- How to define state graphs in LangGraph
- Implementing agents with reasoning and acting (ReAct) patterns
- Adding memory to agents
- Creating conditional edges and loops in graphs
- Handling multiple inputs and outputs
- Building sequential and complex workflows

## Dependencies

See `requirements.txt` for the complete list of packages. Key dependencies include:
- langgraph
- langchain
- langchain_groq
- chromadb
- ipython

## Notes

- The `conversation_history.txt` and `.env` files are intentionally ignored by Git (see `.gitignore`)
- This is a learning project and may contain experimental code
- Feel free to explore, modify, and extend the examples

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Groq Documentation](https://console.groq.com/docs)

Happy learning!