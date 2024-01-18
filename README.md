
# 🌟 GPT-4 Enhanced AI Assistant with YOLOv8, Speech Capabilities, and Web Browsing 

Welcome to the repository of our cutting-edge AI assistant project, where we've empowered GPT-4 with YOLOv8 object detection, speech recognition, text-to-speech, and advanced web browsing functionalities. This project is built using Flask, Langchain, and async programming, offering a seamless and interactive AI experience.

## 📹 Video Demo
https://github.com/HugoLB0/gpt-4-jarvis/assets/66400773/11018f76-d908-4ffb-a0d4-272441a6c5b7



## 🚀 Features 🚀

- **YOLOv8 Integration**: Harnessing the power of the latest YOLOv8 for real-time object detection.
- **Speech Recognition**: Enabled speech-to-text capabilities for natural user interactions.
- **Text-to-Speech**: Converting AI responses into natural, human-like speech.
- **Advanced Web Browsing**: Utilizing browsing tool for extensive online research and information retrieval.
- **Flask Framework**: Robust and scalable web framework for backend services.
- **Langchain**: Leveraging Langchain for seamless integration of language models.
- **Asynchronous Programming**: Ensuring efficient and fast response times.

## ⚙️ Installation ⚙️
### file structure:
- ``` MAIN_FLASK.py ``` is the main script that act as a backend. it handle the requests, Yolo and so on. 
- ``` MAIN_user_cli_gpt.py ``` is the command line version of the client, without the tts and stt feature.
- ``` MAIN_user_speech_reco.py ``` is the client with the stt and tts feature.

### how to run ?
First you have to put your OPENAI_APIKEY in the .env file with the following format:
```
OPENAI_API_KEY="sk-********"
```
Then install required modules (i recommande setting up a virtual environement first):
```
pip install -r requirements.txt
```
Now, run the ``` MAIN_flask.py```, and in another terminal window, run the ``` MAIN_user_cli_gpt.py ``` or ``` MAIN_user_speech_reco.py ```, depending if you want tts and stt feature or not.
```
python MAIN_flask.py
```
```
python MAIN_user_cli_gpt.py # or MAIN_user_speech_reco.py
```




## 📫 Contact me for more informations or if you need any help : 
- Email: hugolebelzic@protonmail.com
- LinkedIn: https://www.linkedin.com/in/hugo-le-belzic-4aa68a207/
