from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


def chat_node(state: ChatState):

    # Take messages from state
    messages = state['messages']

    # Send messages to LLM
    response = llm.invoke(messages)

    # Store AI response in state
    return {
        'messages': [response]
    }


cheackpointer=MemorySaver()
graph = StateGraph(ChatState)

# Add node
graph.add_node('chat_node', chat_node)

# Add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


# Compile graph
chatbot = graph.compile(checkpointer=cheackpointer)


initial_state = {
    'messages': [
        HumanMessage(content='What is the capital of India?')
    ]
}


# print( chatbot.invoke(initial_state)['messages'][-1].content)

thread_id='1'
while True:
    user_message=input("Tupe Here:")

    print('user:',user_message)

    if user_message.strip().lower() in ['exit','bye','quit']:
        break

    config={'configurable':{'thread_id':thread_id}}

    response=chatbot.invoke({'messages':[HumanMessage(content=user_message)]},config=config)

    print("AI:", response["messages"][-1].content[0]["text"])


 