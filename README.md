# AI_Talking


* Pre-requisite / Requiremnts

# AI_Talking

AI_Talking is a lightweight interactive assistant that records audio from your
microphone, transcribes it with Whisper, generates a short LLM response via
Ollama, synthesizes speech using `espeak` (or `espeak-ng`), and plays the
result back to you.

## Features

- Record audio from your microphone interactively
- Transcribe speech using OpenAI Whisper (`base.en` model)
- Generate short responses / suggestions using an Ollama LLM
- Synthesize and play audio using `espeak` via a simple TTS wrapper

## Requirements

- Python 3.10+ recommended
- System packages: `espeak` or `espeak-ng` (for TTS)
- A working microphone and audio output device

Python packages (install inside a virtualenv):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Manual system dependency steps
```bash
  sudo apt install -y python3-venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install sounddevice
  pip3 install numpy
  #pip3 install whisper ### DONT Install
  python -m pip uninstall -y whisper
  pip3 install rich
  pip3 install langchain
  pip3 install langchain.memory
  pip3 install ConversationBufferMemory
  pip3 install langchain langchain-community
  python3 ./play.py
  python3 ./play.py
  python3 ./play.py
  pip3 install tts
  sudo apt install -y espeak
  python3 ./play.py
  pip3 uninstall -u whisper
  pip3 uninstall -y whisper
  pip3 install -U openai-whisper
  python3 ./play.py
  ollama list
  ollama ps
  python3 ./play.py
  deactivate
```

Notes:
- Dependencies are pinned in `requirements.txt` for reproducible installs. Current pinned versions:

```text
numpy==1.26.4
sounddevice==0.4.8
openai-whisper==20230314
torch==2.2.0
rich==13.6.0
langchain==0.0.352
langchain-community==0.0.9
```
- The code loads Whisper with `whisper.load_model("base.en")` (CPU by default). Set FP16/GPUs in `translate.py` if you have GPU support.
- `Ollama` from `langchain_community.llms` is used for the LLM; you need a running Ollama instance and appropriate models for it to work.

## Quick Start

Run the assistant:

```bash
python3 play.py
```

Controls and behavior:

- When the program runs it prompts you to press Enter to start recording.
- Press Enter once to begin recording, then press Enter again to stop.
- The audio is transcribed; the assistant may first produce a short random
	suggestion/question/advice and play it, then generate a reply and play it.
- Press Ctrl+C to exit.

## How it works (high level)

- `play.py` contains the interactive loop: it starts a recording thread,
	collects raw audio bytes, converts them to a NumPy array, and calls into
	functions in `translate.py`.
- `translate.py` handles recording (`record_audio`), transcription
	(`transcribe`) using Whisper, LLM calls (`get_llm_response`, `get_random_prompt`),
	and playback (`play_audio`) via `sounddevice`.
- `chain.py` defines a minimal `SimpleConversationChain` around an Ollama
	LLM and provides a `TextToSpeechService` instance (imported as `tts`) used
	by `play.py` to synthesize long-form speech.
- `tts.py` generates a WAV via `espeak` (or `espeak-ng`) and returns a NumPy
	float array that `sounddevice` can play.

## Troubleshooting

- If you see `TTS engine not found`, install `espeak`:

```bash
sudo apt install -y espeak
```

- If no audio is recorded, confirm your microphone works and `sounddevice`
	can access it. Try running a small test recording with `sounddevice`.
- Ollama LLM calls require a configured Ollama service and model; check
	your Ollama server and model availability with `ollama list` and `ollama ps`.

## Development

- The main files are `play.py`, `translate.py`, `chain.py`, and `tts.py`.
- To change the Whisper model or LLM prompt template, edit `chain.py` or
	the call sites in `translate.py`.

## License

This project does not include a license file. Add one if you plan to share
or publish the code.
