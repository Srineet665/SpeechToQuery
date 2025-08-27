"""Simple GUI application to convert speech into an OMOP SQL query."""

import os
import tempfile
import wave
from typing import Optional

import sounddevice as sd
import openai
import tkinter as tk
from tkinter import messagebox

from speech_to_omop import speech_to_omop_query


def record_audio(seconds: int = 5, samplerate: int = 16000) -> str:
    """Record audio from the system microphone and save to a temporary WAV file.

    Parameters
    ----------
    seconds: int
        Duration to record.
    samplerate: int
        Sampling rate in Hertz.

    Returns
    -------
    str
        Path to the temporary WAV file containing the recording.
    """
    recording = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())
    return tmp.name


def start_recording() -> None:
    """Record audio, convert to an OMOP query, and display the result."""
    label.config(text="Recording... Please speak now.")
    root.update()
    audio_file = record_audio()
    try:
        query = speech_to_omop_query(audio_file)
    finally:
        try:
            os.unlink(audio_file)
        except OSError:
            pass
    label.config(text="OMOP SQL query:")
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, query)


# Ensure API key is available
api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
if not api_key:
    messagebox.showerror("Missing API Key", "Please set the OPENAI_API_KEY environment variable.")
    raise SystemExit(1)
openai.api_key = api_key

# Build simple GUI
root = tk.Tk()
root.title("Speech to OMOP Query")
root.geometry("600x400")

label = tk.Label(root, text="Click 'Start' and speak your query")
label.pack(pady=10)

start_button = tk.Button(root, text="Start", command=start_recording)
start_button.pack(pady=5)

text_box = tk.Text(root, wrap="word")
text_box.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()
