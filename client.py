#client.py

import streamlit as st
import requests

from speak_module import speak
from main import load_excuses, save_excuse, delete_excuse, toggle_favorite, toggle_like
# Constants
API_URL = "http://127.0.0.1:8000"

# Streamlit UI
st.title("📝 Excuse Generator")
st.write("Enter a scenario, and I'll generate a unique excuse and supporting proof.")

input_text = st.text_area("Scenario:")

# Generate excuse and proof
if st.button("Generate Excuse"):
    try:
        # Generate excuse
        if not input_text:
            st.error("❌ Please enter a scenario.")
            st.stop()
        with st.spinner("Generating excuse..."):
            previous_excuses = load_excuses()
            previous_excuses_text = [excuse['text'] for excuse in previous_excuses if 'text' in excuse]
            response = requests.post(f"{API_URL}/excuse", json={"input": input_text, "previous_excuses": previous_excuses_text})
            if response.status_code == 200:
                excuse = response.json()["excuse"]
                st.success(f"🧠 **Generated Excuse:**\n{excuse}")
                st.write("Now, generating proof...")
            else:
                st.error("❌ Error generating excuse.")
                st.stop()

        # Generate proof
        with st.spinner("Generating proof..."):
            proof_response = requests.post(f"{API_URL}/proof", json={"input": excuse})
            if proof_response.status_code == 200:
                proof = proof_response.json()["proof"]
                st.success(f"📄 **Generated Proof:**\n{proof}")
                if excuse != "Error generating proof" and proof != "Error generating proof":
                    save_excuse(excuse, proof)
                    st.info("✅ Excuse and proof saved successfully!")
            else:
                st.error("❌ Error generating proof.")
    except Exception as e:
        st.error(f"❌ {str(e)}")

# Show History of Excuses
st.title("📜 Excuse History")
excuses = load_excuses()

# Add filters
filter = st.selectbox(
    "Filter Excuses",
    options=["All","Favorites","Liked", "Disliked"],
    index=0,
    placeholder="Select a filter",
    help="Filter excuses by favorites or like/dislike status."
)

if excuses:
    for idx, item in enumerate(excuses):
        # 🔥 Filter Favorites
        if filter == "Favorites" and item.get("favorite", True):
            continue
        # 🔥 Filter Like/Dislike
        like_state = item.get("like", None)
        if filter == "Liked" and like_state != True:
            continue
        elif filter == "Disliked" and like_state != False:
            continue

        # --- Display Excuse ---
        st.markdown(f"\n\n'{item['text']}'\n(Timestamp: {item['timestamp']})\n\n")
        st.write(f"Proof: {item['proof']}")
        
        spacer1, col1, col2, col3, col4, spacer2 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1])

        # Favorite button
        with col1:
            favorite_button_label = "Unfavorite" if item.get("favorite", False) else "Favorite"
            if st.button(favorite_button_label, key=f"fav_{idx}"):
                if toggle_favorite(idx):
                    st.success(f"Excuse {idx} marked as {'favorite' if not item['favorite'] else 'unfavorite'}.")
                    st.experimental_rerun()

        # Delete button
        with col2:
            if st.button("🗑️ Delete", key=f"delete{idx}"):
                if delete_excuse(idx):
                    st.success(f"Excuse {idx} deleted.")
                    st.experimental_rerun()

        # Like/Dislike button
        with col3:
            if like_state is None:
                like_button_label = "❤️ Like"
            elif like_state is True:
                like_button_label = "👍 Liked"
            else:
                like_button_label = "👎 Disliked"
            if st.button(like_button_label, key=f"like_{idx}"):
                if toggle_like(idx):
                    st.experimental_rerun()

        # Text-to-Speech button
        with col4:
            if st.button("🔊", key=f"read_{idx}"):
                try:
                    speak(item['text'])
                    st.success(f"Speaking: {item['text']}")
                except Exception as e:
                    st.error(f"Error in text-to-speech: {str(e)}")
else:
    st.write("No excuses found.")
