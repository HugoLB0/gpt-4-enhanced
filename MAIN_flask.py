
# ------ utils ------
import MODULE_object_recognition
import MODULE_text_to_speech_OPENAI

import openai
import asyncio
import flask
import os
from dotenv import load_dotenv 
import json
import threading
import logging
import warnings

load_dotenv() # load api keys

# just to remove useless logs
warnings.filterwarnings("ignore")
logging.getLogger('werkzeug').setLevel(logging.ERROR)

logging.basicConfig(level=logging.INFO, format="[-] %(name)s: %(asctime)s - %(levelname)s - %(message)s")
logging.info(f"[+] Starting {__name__}")

# -- OpenAI settings -- 
OPENAI_CLIENT = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_GPT_PROMPT = "YOU are an IA assistant. for each prompt, you will be given the following data: 'detected_objects' which is the objects detected by the yolo model and 'user_input' which is the input from the user. For each prompt you have to answer or execute the task like an assistant.Internet browsing MAY be necessary. ALl outputs will be in a VALID JSON format: {\"output\": \"output\"}" # 

OPENAI_ASSISTANT = OPENAI_CLIENT.beta.assistants.create(
    name="JPO-GPT-4",
    instructions=OPENAI_GPT_PROMPT,
    tools=[{"type": "retrieval"}],
    model="gpt-4-1106-preview"
)

# initialize OpenAI thread 
# create new thread or import a current one that is working well
#OPENAI_ASSISTANT_THREAD = OPENAI_CLIENT.beta.threads.create()
OPENAI_ASSISTANT_THREAD = OPENAI_CLIENT.beta.threads.retrieve("thread_7MF0QRt87xJYWOBGIDn2S7oh") # this version was working well so i keep it


logging.info(f"OpenAi assistant thread number: {OPENAI_ASSISTANT_THREAD.id}")


FLASK_main_app = flask.Flask("JPO-backend")
#FLASK_OTK = secrets.token_hex(16) # un comment it when in production to generate OTP , and don't forget to change the APIKEY in the client
FLASK_OTK = "1234567890"
logging.debug(f"Generated one time secret API key: {FLASK_OTK}")

# -- script variables --
DETECTED_OBJECTS = [None]  # define empty list so we can directly use DETECTED_OBJECTS[0] = data, i can use a str instead but idk 



@FLASK_main_app.route('/MODULE_object_detection', methods=['POST'])
async def FLASK_MODULE_object_detection():
    
    global DETECTED_OBJECTS # i know global is bad 
    
    client_request = flask.request
    FLASK_client_api_key = client_request.headers.get("API-KEY")
    
    logging.debug(f"Received request with API-KEY: {FLASK_client_api_key}")
    if str(FLASK_client_api_key) != str(FLASK_OTK):
        flask.abort(401)
    else:
        FLASK_client_json_payload = client_request.get_json()
        if FLASK_client_json_payload.get("test") == "200":
            logging.info(f"Received test request from MODULE_object_detection")
            return flask.jsonify({"status": "200"})
        
        logging.debug(f"Received request: {FLASK_client_json_payload}")

        DETECTED_OBJECTS[0] = FLASK_client_json_payload 
        return flask.jsonify({"status": "200"})


@FLASK_main_app.route('/MODULE_usercli_input', methods=['POST'])
async def FLASK_MODULE_usercli_input():
    
    client_request = flask.request
    FLASK_client_api_key = client_request.headers.get("API-KEY")
    
    logging.debug(f"Received request with API-KEY: {FLASK_client_api_key}")
    if str(FLASK_client_api_key) != str(FLASK_OTK):
        flask.abort(401)
    else:
        FLASK_client_json_payload = client_request.get_json()
        logging.debug(f"Received user input: {FLASK_client_json_payload}")

        if FLASK_client_json_payload.get("test") == 200:
            logging.info(f"Received test request from MODULE_usercli_gpt")
            return flask.jsonify({"status": "200"})
        else:
            str_user_input = FLASK_client_json_payload.get("text")
            
            result = await PROCESS_data(str_user_input)
            return flask.jsonify(result)



async def PROCESS_data(input_str):
    """
    input data + image detection -> prompt
    prompt -> openai assiatant with browsing
    """
    
    PROCESS_DETECTED_OBJECTS = DETECTED_OBJECTS[0]
    
    logging.info(f"Processing prompt: {input_str}")
    logging.info(f"Detected objects: {PROCESS_DETECTED_OBJECTS}")
    
    processed_data = f"'user_input': {input_str},'detected_objects': {PROCESS_DETECTED_OBJECTS}"
    
    # here i followed the documentation
    OPENAI_ASSISTANT_MESSAGE = OPENAI_CLIENT.beta.threads.messages.create(
        thread_id=OPENAI_ASSISTANT_THREAD.id,
        role="user",
        content=processed_data
    )
    OPENAI_ASSISTANT_RUN = OPENAI_CLIENT.beta.threads.runs.create(
        thread_id=OPENAI_ASSISTANT_THREAD.id,
        assistant_id=OPENAI_ASSISTANT.id,
        instructions=""
        )
    
    OPENAI_TASK = OPENAI_CLIENT.beta.threads.runs.retrieve(
        thread_id=OPENAI_ASSISTANT_THREAD.id,
        run_id=OPENAI_ASSISTANT_RUN.id
        )
    while OPENAI_TASK.completed_at is None:
        OPENAI_TASK = OPENAI_CLIENT.beta.threads.runs.retrieve(
        thread_id=OPENAI_ASSISTANT_THREAD.id,
        run_id=OPENAI_ASSISTANT_RUN.id
        )
        messages = OPENAI_CLIENT.beta.threads.messages.list(
            thread_id=OPENAI_ASSISTANT_THREAD.id
            )
        # some tasks takes longer then others so we have to wait a bit
        await asyncio.sleep(0.1)
    
    response = messages.data[0].content[0].text.value
    logging.info(f"OpenAI response: {response}")

    MODULE_text_to_speech_OPENAI.text_to_speech(str(json.loads(response)['output']))

    return response
    

# START
# cv2.imgshow() is not thread safe so we have to run it here
logging.info("Starting flask server")
threading.Thread(target=lambda: FLASK_main_app.run(host="", port=8888, debug=False,use_reloader=False)).start()
logging.info("Starting object recognition module")
MODULE_object_recognition.main()



