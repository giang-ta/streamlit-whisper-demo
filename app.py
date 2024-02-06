import difflib
import streamlit as st
import os

from whisper import load_model, transcribe
from pathlib import Path
from utils import add_noise, concatenate_text  # Ensure add_noise is imported

NOISE_PATH = "noise/heavy-rain-nature-sounds.mp3"
# Ensure audio directory exists
audio_dir = Path("audio")
audio_dir.mkdir(exist_ok=True)

st.title("Open AI Whisper Demo")

# Initialize or update transcription in session_state if not already present
if 'transcription' not in st.session_state:
    st.session_state['transcription'] = ""

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])
yes_add_noise = st.checkbox('Add noise')

# UI for adding noise
noise_volume = st.slider("Noise Volume", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

if st.button("Upload"):
    if uploaded_file is not None:
        file_path = audio_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("File uploaded successfully!")
        
        if yes_add_noise:
            # Call add_noise function here
            add_noise(str(file_path), str(NOISE_PATH), noise_volume)

files = list(audio_dir.glob("*.*"))
file_names = [file.name for file in files]
selected_file_name = st.selectbox("Or choose from uploaded audios", file_names)

if selected_file_name:
    audio_file_path = str(audio_dir / selected_file_name)
    st.audio(audio_file_path)

    model_type = st.selectbox("Choose Whisper model type", ["tiny", "base", "small", "medium", "large"], key="model_select")

    if st.button("Transcribe Audio"):
        model = load_model(model_type)
        result = model.transcribe(audio_file_path)
        st.session_state.transcription = result["text"]

# Display the generated transcript
st.write("Generated Transcript")
st.text_area("Generated Transcript", value=st.session_state.transcription, height=300, key="generated_transcript", label_visibility="collapsed")

st.write("Original Transcript")
original_transcript = st.text_area("Enter original transcript here to compare:", height=300, key="original_transcript", label_visibility="collapsed")

if st.button("Compare Transcripts", key="compare_button"):
    if original_transcript and st.session_state.transcription:
        similarity = difflib.SequenceMatcher(None, original_transcript, st.session_state.transcription).ratio()
        st.info(f"Matching percentage: {similarity*100:.2f}%")
    else:
        st.warning("Please enter an original transcript to compare.")