#app.py
from fastapi import FastAPI
from agents.excuse_agent import generate_excuse
from agents.proof_agent import generate_proof
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Input model
class InputText(BaseModel):
    input: str
    previous_excuses: List[str] = []

# Initialize the app
@app.post("/excuse")
def get_excuse(data: InputText):
    try:
        print(f"Received input: {data.input}")
        print(f"Previous excuses: {data.previous_excuses}")
        result = generate_excuse(data.input, previous_excuses=data.previous_excuses)
        print(f"Generated excuse: {result}")
        return {"excuse": result}
    except Exception as e:
        print(f"Error while generating excuse: {e}")
        return {"excuse": "Error generating excuse", "proof": "Error generating proof"}

@app.post("/proof")
def get_proof(data: InputText):
    try:
        print(f"Received input for proof generation: {data.input}")
        result = generate_proof(data.input)
        print(f"Generated proof: {result}")
        return {"proof": result}
    except Exception as e:
        print(f"Error while generating proof: {e}")
        return {"proof": "Error generating proof"}


