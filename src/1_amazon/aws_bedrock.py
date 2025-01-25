# Modified from DEV aticle: https://dev.to/aws-builders/creating-a-simple-chatbot-with-context-on-amazon-bedrock-5bi1
import boto3
import json
import os
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain

# Initializing client
client = boto3.client(
    service_name='bedrock-runtime', 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_DEFAULT_REGION'],
)

# Create Langchain instance to keep chat history
memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("You will act as a principal software engineer and answer software engineering questions.")
memory.chat_memory.add_ai_message("I am a principal software engineer and will answer your software engineering questions.")

titan_llm = Bedrock(
    model_id="amazon.titan-text-lite-v1",
    client=client)
conversation = ConversationChain(
     llm=titan_llm, 
     verbose=True, 
     memory=memory
)

# Running prompts
conversation.predict(input="What is the best programming language?")
conversation.verbose = True
conversation.predict(input="What programming languages do you use?")


