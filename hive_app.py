import streamlit as st
import requests

# 1. YOUR GOOGLE WEB APP URL
URL = "https://script.google.com/macros/s/AKfycbz_hLwiW9Q_SVhY4WTvwOzg2fcYxHZGdVAkbQp_jCS3Pnmbldhz1XMf-_Gu-CoSTdeiCw/exec"

st.set_page_config(page_title="Hive Pro", layout="centered")

# --- SMART QR CODE LOGIC ---
# This looks at the URL for "?id=..."
query_params = st.query_params
default_id = query_params.get("id", "") # If URL has ?id=Hive01, it grabs "Hive01"

st.title("🐝 Hive Inspection")

# If ID was in the QR code, it shows up here automatically
hive_id = st.text_input("Hive ID", value=default_id)

st.write("---")
st.markdown("### 📝 Observations")
st.info("💡 Pro Tip: Tap the Microphone icon on your phone's keyboard to speak your notes!")

# Text area where the transcribed text (from your keyboard) goes
notes = st.text_area("Notes", height=150, placeholder="Tap here and use your phone's voice-to-text button...")

# Save Button
if st.button("💾 Save to Google Sheets", use_container_width=True):
    if hive_id and notes:
        payload = {"hive_id": hive_id, "notes": notes}
        try:
            response = requests.post(URL, json=payload)
            if response.status_code == 200:
                st.success(f"✅ Data for {hive_id} saved!")
                st.balloons()
            else:
                st.error("Failed to connect to Google Sheets.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please ensure Hive ID and Notes are filled.")
