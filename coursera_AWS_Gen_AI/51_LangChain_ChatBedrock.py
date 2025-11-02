from langchain_aws import ChatBedrock

chat = ChatBedrock(
    model_id="...",
    temperature=0
)

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(
    content="You are a helpful assistant! Your name is Bob."
    ),
    HumanMessage(
    content="What is your name?"
    )
]

# Define a chat model and invoke it with the messages
print(model.invoke(messages))

from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

prompt_value = template.invoke(
    {
    "name": "Bob",
    "user_input": "What is your name?"
    }
)

