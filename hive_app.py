import streamlit as st
import requests
import time

# --- CONFIG & SECRETS ---
# Accessing the secrets you set in Step 1
GOOGLE_URL = st.secrets["https://docs.google.com/spreadsheets/d/1lrqhtVyzgdbfU1jfNmEVcEEVkGwC-U7keY-2UT6vhmQ/edit?gid=0#gid=0"]
ASSEMBLY_KEY = st.secrets["ASSEMBLYAI_API_KEY"]

st.set_page_config(page_title="Hive API Manager", page_icon="🐝", layout="wide")

# --- FUNCTIONS ---
def transcribe_audio(audio_file):
    """Sends audio to AssemblyAI for transcription"""
    headers = {'authorization': ASSEMBLY_KEY}
    # Upload audio
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=audio_file)
    audio_url = upload_response.json()['upload_url']
    
    # Start Transcription
    trans_response = requests.post('https://api.assemblyai.com/v2/transcript', headers=headers, json={'audio_url': audio_url})
    transcript_id = trans_response.json()['id']
    
    # Wait for result
    while True:
        polling_response = requests.get(f'https://api.assemblyai.com/v2/transcript/{transcript_id}', headers=headers)
        if polling_response.json()['status'] == 'completed':
            return polling_response.json()['text']
        elif polling_response.json()['status'] == 'error':
            return "Transcription Error"
        time.sleep(1)

# --- UI INTERFACE ---
st.title("🐝 Hive API Manager")

tab1, tab2 = st.tabs(["📋 New Inspection", "📜 View History"])

with tab1:
    # 1. Automatic ID from QR code
    query_params = st.query_params
    qr_id = query_params.get("id", "")
    
    col1, col2 = st.columns(2)
    with col1:
        hive_id = st.text_input("Target Hive ID", value=qr_id)
        
    # 2. Voice Section
    st.write("### 🎤 Audio Observation")
    audio_data = st.audio_input("Record your voice note")
    
    # 3. Automatic Transcription Logic
    notes = ""
    if audio_data:
        if st.button("✨ Transcribe Voice"):
            with st.spinner("Converting speech to text..."):
                notes = transcribe_audio(audio_data)
                st.success("Transcribed!")
    
    # Editable Text Box (Manual or Transcribed)
    final_notes = st.text_area("Inspection Notes", value=notes, height=150)
    
    if st.button("🚀 Save to Google Sheet", use_container_width=True):
        if hive_id and final_notes:
            payload = {"hive_id": hive_id, "notes": final_notes}
            res = requests.post(GOOGLE_URL, json=payload)
            if res.status_code == 200:
                st.balloons()
                st.success(f"Log for {hive_id} saved successfully!")
            else:
                st.error("Submission failed.")
        else:
            st.warning("Please provide both Hive ID and Notes.")

with tab2:
    st.write("### Recent Logs")
    st.info("The data is stored in your Google Sheet. Open it here:")
    st.link_button("Go to Google Sheet", "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE")
