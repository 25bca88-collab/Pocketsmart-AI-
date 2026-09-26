POCKETSMART AI - CLEAN START

Extract this folder to:
C:\Users\BASHA\Documents\pocketsmart\pocketsmart-AI

In VS Code Terminal:
python -m pip install -r requirements.txt

Then edit .env and replace PASTE_YOUR_GEMINI_API_KEY_HERE with your NEW Gemini API key.

Start:
python -m uvicorn main:app --reload

Open:
http://127.0.0.1:8000

The app works in demo mode even before a Gemini key is added.
