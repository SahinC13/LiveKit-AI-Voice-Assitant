python -m venv ai
.\ai\Scripts\Activate.ps1
.\ai\Scripts\activate.bat
pip install "livekit-agents[deepgram,openai,cartesia,silero,turn-detector]~=1.0"
pip install "livekit-plugins-noise-cancellation~=0.2"
pip install "python-dotenv"
python main.py download-files
python main.py dev

Make sure to run all these on terminal in order to start.
Note: Used VS Code.
