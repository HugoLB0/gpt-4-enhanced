import requests
import asyncio
import time
import logging
import speech_recognition 
import json
from colorama import Fore
import openai
import os

logging.basicConfig(level=logging.INFO, format="%(name)s: %(asctime)s - %(levelname)s - %(message)s")
logging.info(f"[+] Starting {__name__}")


# define microphone
SPEECH_RECOGNIZER = speech_recognition.Recognizer()
OPENAI_CLIENT = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# for interaction with the backend
r_headers ={
    "content-type": "application/json",
    'API-KEY': "1234567890"
}


mainloop_endpoint = "http://127.0.0.1:8888/MODULE_usercli_input"


async def main():
    print("Using microphone", speech_recognition.Microphone.list_microphone_names())
    
    while True:
        time.sleep(0.2)
        try:
            r = requests.post(mainloop_endpoint, headers=r_headers, json={"test": 200})
            break
        except Exception:
            logging.debug("Waiting for flask server to start")
    
    
    while True:
        with speech_recognition.Microphone() as AUDIO_SOURCE:  
            logging.info("Say something!")
            LISTENER = SPEECH_RECOGNIZER.listen(
                AUDIO_SOURCE, 
                timeout=5, 
                phrase_time_limit=5)
            
        logging.info("Recognizing...")
        with open('temp.wav', 'wb') as TEMP_AUDIO_FILE:
            TEMP_AUDIO_FILE.write(LISTENER.get_wav_data())
        TEMP_AUDIO_FILE.close()
            
        AUDIO_FILE_DATA = open('temp.wav', 'rb')
            
        RECOGNIZED_TEXT = OPENAI_CLIENT.audio.translations.create(
            model="whisper-1", 
            file=AUDIO_FILE_DATA,
            response_format="text"
            )

        logging.info("Recognized text: " + RECOGNIZED_TEXT)
            
        usercli_r = requests.post(mainloop_endpoint, json={"text": RECOGNIZED_TEXT}, headers=r_headers)
        try:
            response = usercli_r.json()
            response = json.loads(response)['output']
        except Exception:
            response = usercli_r.text
        logging.info(f"Response: {response}")
        os.remove('temp.wav')


    
if __name__ == "__main__":
    asyncio.run(main())