"""Speech to OMOP query utility."""

import os
from typing import Optional

try:
    import openai
except ImportError as exc:  # pragma: no cover - library required at runtime
    raise SystemExit("The openai package is required to run this script.") from exc


def transcribe_audio(path: str, model: str = "whisper-1") -> str:
    """Transcribe an audio file to text using OpenAI's Whisper model.

    Parameters
    ----------
    path: str
        Path to a local audio file (e.g. WAV, MP3).
    model: str, optional
        Whisper model name.

    Returns
    -------
    str
        Transcribed text.
    """
    with open(path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(model=model, file=audio_file)
    return transcript["text"].strip()


def generate_omop_query(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Generate an OMOP SQL query from natural language."""
    system_message = (
        "You translate natural language requests into SQL queries for the OMOP "
        "Common Data Model. Only output SQL without explanations."
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"].strip()


def speech_to_omop_query(audio_path: str) -> str:
    """Convert speech in ``audio_path`` to an OMOP SQL query."""
    text = transcribe_audio(audio_path)
    return generate_omop_query(text)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert speech to an OMOP SQL query.")
    parser.add_argument("audio", help="Path to audio file to transcribe and convert")
    args = parser.parse_args()

    api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Please set the OPENAI_API_KEY environment variable.")
    openai.api_key = api_key

    print(speech_to_omop_query(args.audio))
