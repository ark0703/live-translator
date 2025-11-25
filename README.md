
# live-translator
Live-translator is a small Python application that takes live voice input from your microphone,
translates the detected text into another language, and speaks the translated text back.

Features
- Real-time voice-to-voice translation between languages supported by googletrans.
- Uses Google Speech Recognition to convert spoken words to text.
- Text translation via `googletrans` (supports sync or async implementations).
- Converts translated text to speech using `gTTS`.
- Plays audio output with `pygame`.
- Simple DearPyGui user interface for starting/stopping and viewing conversation text.

Dependencies
- Python 3.8+ recommended
- gTTS
- googletrans (note: different versions/implementations may be sync or async)
- SpeechRecognition
- PyAudio (for microphone access) or alternative microphone backends
- pygame
- dearpygui

Quick setup (Windows / PowerShell)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (you can pin versions as needed).
```powershell
python packacges.py
```

Notes on googletrans
- The `googletrans` ecosystem includes several forks and versions; some return results synchronously while
	others expose async APIs. If you expect synchronous behavior, pin to a known sync release such as
	`googletrans==4.0.0-rc1`. The project code already handles both sync and awaitable translate() return values.

How to run
1. From the project folder (where `Interface.py` lives) run:

```powershell
python .\Interface.py
```

2. Enter the language names (e.g. `english`, `hindi`) in the GUI fields and click Start.
3. The program will listen to the microphone, display the recognized text, translate it, and speak the translation.

Files of interest
- `Interface.py` — GUI and main loop.
- `translator_modules.py` — voice capture, translation, TTS, and playback helpers.
- `packages.py` — helper script to install dependencies (optional).

Troubleshooting
- Microphone access: ensure your OS and Python have permission to access the microphone.
- PyAudio install issues: on Windows, prebuilt wheels for PyAudio can be easier to install (search for "PyAudio wheels").
- If you see async-related errors from `googletrans`, try pinning the package version as shown above.
- If audio won't play, verify `pygame` is installed and that your system audio device is available.

License & notes
- This is a small demo/side project. If you plan to distribute, please follow the terms of use for the
	Google services used (Speech Recognition and Google Translate APIs).

