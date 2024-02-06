import os
import librosa
import numpy as np
import soundfile as sf


def add_noise(original_path: str, noise_path: str, noise_volume: float=0.5) -> None:
    # Load original audio file
    audio_path = original_path
    audio, sr = librosa.load(audio_path, sr=None)

    # Load noise file (ensure it has the same sample rate as your original audio)
    noise_path = noise_path
    noise, _ = librosa.load(noise_path, sr=sr)

    # If the noise clip is shorter than the original audio, loop it
    if len(noise) < len(audio):
        noise = np.tile(noise, int(np.ceil(len(audio)/len(noise))))

    # Trim the noise clip to match your audio length
    noise = noise[:len(audio)]

    # Adjust the volume of the noise (0.1 is an example scaling factor for the noise volume)
    scaled_noise = noise * noise_volume

    # Mix audio with noise
    mixed_audio = audio + scaled_noise

    # Ensure the mixed audio is not clipping
    mixed_audio = np.clip(mixed_audio, -1.0, 1.0)

    # Save the mixed audio to a file
    output_path = f"audio/noisy_{os.path.basename(original_path)}"
    sf.write(output_path, mixed_audio, sr)

def concatenate_text(text: str) -> str:
    # Split the text into paragraphs, remove newlines and concat
    paragraphs = text.split('\n')
    concatenated_text = ' '.join(paragraph.strip() for paragraph in paragraphs if paragraph)
    return concatenated_text