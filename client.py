# client.py
import streamlit as st
from agents.excuse_agent import generate_excuse
from agents.proof_agent import generate_proof
from speak_module import speak
import json
import os
from datetime import datetime

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


st.title("📝 Excuse Generator")
st.write("Enter a scenario, and I'll generate a unique excuse and supporting proof.")

input_text = st.text_area("Scenario:")

if st.button("Generate Excuse"):
    try:
        if not input_text:
            st.error("❌ Please enter a scenario.")
            st.stop()

        with st.spinner("Generating excuse..."):
            previous_excuses = load_excuses()
            previous_excuses_text = [excuse['text'] for excuse in previous_excuses if 'text' in excuse]
            excuse = generate_excuse(input_text, previous_excuses_text)
            st.success(f"🧠 **Generated Excuse:**\n{excuse}")

        with st.spinner("Generating proof..."):
            proof = generate_proof(excuse)
            st.success(f"📄 **Generated Proof:**\n{proof}")
            if excuse != "Error generating proof" and proof != "Error generating proof":
                save_excuse(excuse, proof)
                st.info("✅ Excuse and proof saved successfully!")

    except Exception as e:
        st.error(f"❌ {str(e)}")

# Show Excuse History
st.title("📜 Excuse History")
excuses = load_excuses()

filter = st.selectbox("Filter Excuses", options=["All", "Favorites", "Liked", "Disliked"], index=0)

if excuses:
    for idx, item in enumerate(excuses):
        # Filtering
        if filter == "Favorites" and not item.get("favorite", False):
            continue
        if filter == "Liked" and item.get("like") != True:
            continue
        if filter == "Disliked" and item.get("like") != False:
            continue

        st.markdown(f"**'{item['text']}'**  \n_Timestamp_: {item['timestamp']}")
        st.write(f"Proof: {item['proof']}")
        
        spacer1, col1, col2, col3, col4, spacer2 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1])

        with col1:
            favorite_button_label = "Unfavorite" if item.get("favorite", False) else "Favorite"
            if st.button(favorite_button_label, key=f"fav_{idx}"):
                toggle_favorite(idx)
                st.experimental_rerun()

        with col2:
            if st.button("🗑️ Delete", key=f"delete{idx}"):
                delete_excuse(idx)
                st.experimental_rerun()

        with col3:
            like_state = item.get("like", None)
            like_button_label = "❤️ Like" if like_state is None else ("👍 Liked" if like_state else "👎 Disliked")
            if st.button(like_button_label, key=f"like_{idx}"):
                toggle_like(idx)
                st.experimental_rerun()

        with col4:
            if st.button("🔊", key=f"read_{idx}"):
                try:
                    speak(item['text'])
                    st.success(f"Speaking: {item['text']}")
                except Exception as e:
                    st.error(f"Error in text-to-speech: {str(e)}")
else:
    st.write("No excuses found.")
