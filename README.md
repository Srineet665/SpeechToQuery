# SpeechToQuery

This prototype turns spoken queries into SQL against the **OMOP** Common Data Model.
It uses OpenAI's Whisper model for transcription and a chat model to translate the
transcribed text into an OMOP SQL query.

## Requirements

- Python 3.11+
- An OpenAI API key available as `OPENAI_API_KEY`
- `openai` Python package (see `requirements.txt`)

Install dependencies with:

```
pip install -r requirements.txt
```

## Usage

```
python speech_to_omop.py path/to/audio_file.wav
```

The script prints a SQL query. The output assumes the target database implements
the OMOP Common Data Model and is intended as a starting point that may require
validation before execution.

### GUI application

For an interactive application that records audio from your microphone, run:

```
python app.py
```

A small window will open. Click **Start**, speak your query, and the resulting
OMOP SQL will be displayed.
