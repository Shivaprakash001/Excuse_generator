# proof_agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# This function generates a proof document based on the input excuse.
def generate_proof(input):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            Pick one of the following proof document types: mail, chat history, call log, location log.
            You are an expert in generating fake proof documents — choose the one most suitable for the excuse.
            Your task is to create a realistic proof document based on the given excuse.
            The output should contain only one proof document, without any additional explanations or context.
        """),
        ("user", "Excuse: {input}")
    ])
    
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0.4,
        max_tokens=120
    )

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"input": input})
    return response
