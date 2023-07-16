import webbrowser
import requests
import json
import playsound
import os
import win32api
import pyaudio
import wave
import threading
from aip import AipSpeech
from pynput.keyboard import Listener


prologue = '主人您好，我是Niubility，爱你哦~'  # 开场白

"""图灵机器人API"""
urls = 'http://openapi.tuling123.com/openapi/api/v2'
key = '**********'
api_key = '490aac3d1e89447297ed96204d0bc780'

count = 1   # 计数
run = False

"""pyaudio参数"""
CHUNK = 1024    # 数据包或者数据片段
FORMAT = pyaudio.paInt16    # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
CHANNELS = 1    # 声道，1为单声道，2为双声道
RATE = 16000    # 采样率，每秒钟16000次
# RECORD_SECONDS = 5  # 录音时间
WAVE_OUTPUT_FILENAME = "output.wav"     # 保存录音文件名

""" 你的 APPID AK SK """
APP_ID = '36216107'
API_KEY = 'rqtwrF0G6pkgjphrL6z6Yk4s'
SECRET_KEY = 'NVRsxw30gvwcytbSNfXm51D0o8oY1W97'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)		# 百度语音接口

def recoder():
    _frames = []
    global run
    p = pyaudio.PyAudio()
    stream = p.open(channels=CHANNELS,
                    format=FORMAT,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    while run:
        data = stream.read(CHUNK)
        _frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(_frames))
    wf.close()
    # print("Saved")

# 按键按下空格时控制录音功能开关
def press(key):
    global run
    try:
        # print(str(key))
        if str(key) == 'Key.space':
            run = not run

            # print(run)
    except AttributeError as e1:
        print(e1)
        pass

# 监听键盘
def check_input():
    with Listener(on_press=press) as listener:
        listener.join()


# 读取录音文件字节码
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别录音,语音转文字
def lic():
    res = client.asr(get_file_content(WAVE_OUTPUT_FILENAME), 'wav', 16000, {
        'dev_pid': 1537,
    })
    text = res['result'][0]
    # print(text)
    return text

# 语音合成
def speak_(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
        'per': 0,
        'spd': 5,
        'pit': 5
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
        playsound.playsound('audio.mp3')
        os.remove('audio.mp3')

# 第一层判别
def respond(data):

    if '歌' in data:
        douban_rul = 'https://douban.fm/'
        webbrowser.get().open(douban_rul)
    elif '搜索' in data:
        _, keywords = data.split('搜索')
        baidu_url = 'https://www.baidu.com/s?wd=' + keywords
        webbrowser.get().open(baidu_url)
    elif '打开' in data:
        _, name = data.split('打开')
        # print(name)
        if '网易云' in name:
            win32api.ShellExecute(0, 'open', 'D:\App\CloudMusic\cloudmusic.exe', '', '', 1)    # 打开网易云
        elif 'QQ' in name or 'qq' in name:
            win32api.ShellExecute(0, 'open', r'D:\App\QQ\Bin\QQScLauncher.exe', '', '', 1)    # 打开QQ
        elif '微信' in name:
            win32api.ShellExecute(0, 'open', r'D:\App\WeChat\WeChat.exe', '', '', 1)   # 打开微信

    else:
        data_dict = {
            "reqType":0,
            "perception": {
                "inputText": {
                    "text": data
                },
            },
            "userInfo": {
                "apiKey": api_key,
                "userId": "！！！你自己的userId！！！ "
            }
        }
        result = requests.post(urls, json=data_dict)
        content = (result.content).decode('utf-8')
        # print(content)
        ans = json.loads(content)
        text = ans['results'][0]['values']['text']
        print('Niubility:',text)
        speak_(text)


if __name__ == '__main__':

    print('Niubility:', prologue)
    speak_(prologue)
    print('{}//你:按  空格  键开始说话...'.format(count), end=' ')

    t1 = threading.Thread(target=check_input,args=())      # 监听键盘
    t1.start()

    while 1:

        if run is True:
            print('\r{}//你:正在听呢，说完了请再按  空格  键...'.format(count), end=' ')
            recoder()
            text2 = lic()
            print('\r{}//你:'.format(count),text2)
            respond(text2)
            count += 1
            print('{}//你:按  空格  键开始说话...'.format(count), end=' ')
