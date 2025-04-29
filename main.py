#main.py
# This script serves as the main entry point for the application.
import os
import json
from datetime import datetime
import subprocess
import sys
import threading
import time

DATA_FILE = "excuses.json"

# Load existing excuses from the file
def load_excuses():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# Save a new excuse to the file
def save_excuse(excuse, proof, favorite=False, like=None):
    new_excuse = {
        "text": excuse,
        "proof": proof,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "favorite": favorite,
        "like": like,
    }
    
    # Load existing excuses and append the new one
    data = load_excuses()
    data.append(new_excuse)
    
    # Save the updated data back to the file
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# Delete an excuse by index
def delete_excuse(index):
    data = load_excuses()
    if index < len(data):
        data.pop(index)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

# Mark an excuse as a favorite
def toggle_favorite(index):
    data = load_excuses()
    if index < len(data):
        data[index]["favorite"] = not data[index]["favorite"]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2) 

# Toggle like/dislike state
def toggle_like(index):
    data = load_excuses()
    if index < len(data):
        current_like = data[index].get("like", None)
        if current_like is None:
            data[index]["like"] = True  # Liked
        elif current_like is True:
            data[index]["like"] = False  # Disliked
        else:
            data[index]["like"] = None  # Reset to neutral (null)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)



# Step 1: Install dependencies
def install_dependencies():
    print("🔧 Installing dependencies from requirements.txt...")
    try:
        subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], check=True)
    except Exception as e:
        print(f"⚠️ Failed to install dependencies: {e}")

# Step 2: Run the FastAPI server (app.py)
def run_fastapi_server():
    print("🚀 Starting FastAPI server...")
    subprocess.run([sys.executable, "-m", "uvicorn", "app:app", "--reload"])

# Step 3: Run the Streamlit client (client.py)
def run_streamlit_client():
    print("🖥️ Starting Streamlit client...")
    subprocess.run([
        "streamlit", 
        "run", 
        "client.py", 
        "--server.address=0.0.0.0", 
        "--server.port=8501"
    ])



if __name__ == "__main__":
    # Install all requirements
    install_dependencies()

    # Start the FastAPI backend server in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi_server, daemon=True)
    fastapi_thread.start()

    # Wait a few seconds to make sure FastAPI server is up
    time.sleep(3)

    # Start the Streamlit frontend
    run_streamlit_client()