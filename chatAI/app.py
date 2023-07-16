from io import StringIO
from pathlib import Path
import streamlit as st
from streamlit_chat import message

import time
#from detect import detect
import os
import sys
import argparse
from PIL import Image
import webbrowser
import requests
import json
import playsound
import os
#import win32api
#import pyaudio
import wave
import threading
#from aip import AipSpeech
#from pynput.keyboard import Listener
# chat_bot.py


# 申请的api_key

prologue = '主人您好，我是Niubility，爱你哦~'  # 开场白

"""图灵机器人API"""
urls = 'http://openapi.tuling123.com/openapi/api/v2'
api_key = '490aac3d1e89447297ed96204d0bc780'

count = 1   # 计数
run = False

"""pyaudio参数"""
CHUNK = 1024    # 数据包或者数据片段
#FORMAT = pyaudio.paInt16    # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
CHANNELS = 1    # 声道，1为单声道，2为双声道
RATE = 16000    # 采样率，每秒钟16000次
# RECORD_SECONDS = 5  # 录音时间
WAVE_OUTPUT_FILENAME = "output.wav"     # 保存录音文件名

""" 你的 APPID AK SK """
APP_ID = '36216107'
API_KEY = 'rqtwrF0G6pkgjphrL6z6Yk4s'
SECRET_KEY = 'NVRsxw30gvwcytbSNfXm51D0o8oY1W97'

#client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)		# 百度语音接口
def AIrespond(data):
  data_dict = {
      "reqType":0,
        "perception": {
            "inputText": {
                "text": data
            },
        },
        "userInfo": {
            "apiKey": api_key,
            "userId": "584403"
        }
  }

  result = requests.post(urls, json=data_dict)
  content = (result.content).decode('utf-8')
    # print(content)
  ans = json.loads(content)
  text = ans['results'][0]['values']['text']
  return text



st.session_state['generated'] = []
st.session_state['past'] = []

st.markdown("#### 我是ChatGPT聊天机器人,我可以回答您的任何问题！")
user_input = st.text_input("请输入您的问题:", key='input')
while True:
    if st.button('发送'):
        st.write("USER:" + user_input)
        output=AIrespond(user_input)
        st.write("AI:"+output)

