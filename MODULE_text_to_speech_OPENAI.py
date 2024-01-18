import playsound
import logging
import openai
import warnings
import os
from pathlib import Path
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.DEBUG, format="[-] %(name)s: %(asctime)s - %(levelname)s - %(message)s")
logging.info(f"[+] Starting {__name__}")

OPENAI_CLIENT = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def text_to_speech(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = OPENAI_CLIENT.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
    )
    
    response.stream_to_file(speech_file_path)
    playsound.playsound(speech_file_path)
    os.remove(speech_file_path)
    
    