# excuse_agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Function to generate excuse
def generate_excuse(input, previous_excuses):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You're a smart assistant generating short, natural responses to scenarios.

For each input:
- Decide if it needs an apology, excuse, or both mostly go with excuse.
- Response must be human-like, realistic, and suitable for the context.
- Avoid repeating anything from the previous responses (JSON list).
- Analyze the previous excuses and try to make it different from them and it included user feedback that will help you in improve responses.
- Just provide the excuse or apology, no extra suggestions.
- make a story out of it.
- Try to explain the situation in a way that makes sense.

Keep it concise (1–2 lines). Output only the response text.

Previous responses:
{previous_excuses}
"""),
        ("user", "Scenario: {input}")
    ])

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0.3,
        max_tokens=80
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    response = chain.invoke({
        "input": input,
        "previous_excuses": previous_excuses
    })
    return response
