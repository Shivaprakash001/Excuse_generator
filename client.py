# client.py
import streamlit as st
from agents.excuse_agent import generate_excuse
from agents.proof_agent import generate_proof
from speak_module import speak
from main import load_excuses, save_excuse, delete_excuse, toggle_favorite, toggle_like

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
