import streamlit as st
import requests

# 1. YOUR GOOGLE WEB APP URL (From the Apps Script "Deploy" step)
URL = "https://script.google.com/macros/s/AKfycbz_hLwiW9Q_SVhY4WTvwOzg2fcYxHZGdVAkbQp_jCS3Pnmbldhz1XMf-_Gu-CoSTdeiCw/exec"

st.set_page_config(page_title="Hive Logger", layout="centered")
st.title("🐝 Hive Inspection")

# Input Fields
hive_id = st.text_input("Hive ID / Number")
notes = st.text_area("Observations", placeholder="Talk or type here...")

# Voice Input (This works on phones!)
st.write("🎤 Record a Voice Note:")
audio_data = st.audio_input("Record your voice")

if audio_data:
    st.audio(audio_data)
    st.info("Note: To keep this 100% free, the audio is recorded above. Usually, transcription requires a paid API (like OpenAI). For now, you can listen back to this or type the summary above.")

# Save Button
if st.button("Submit to Google Sheets"):
    if hive_id:
        payload = {"hive_id": hive_id, "notes": notes}
        try:
            response = requests.post(URL, json=payload)
            if response.status_code == 200:
                st.success("✅ Data saved to Google Sheets!")
                st.balloons()
            else:
                st.error("Error: Could not connect to Google.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
    else:
        st.warning("Please enter a Hive ID.")