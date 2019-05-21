import wave
import pyaudio
import os
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '15920162'
API_KEY = 'kbpGI9bdy39Isbn7sQQGzQQV'
SECRET_KEY = 'jZ6N1ti0GyzPWGeuooU3ing7flHjjrWh'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 定义数据流块
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# 录音时间
RECORD_SECONDS = 5
# 要写入的文件名
WAVE_OUTPUT_FILENAME = "C:/Users/pc/Desktop/program_edit/program/audio/output.wav"

# 读取文件
def get_file_content(filePath):
    cmd_str = "ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm"%(filePath,filePath)
    os.system(cmd_str)  # 调用系统命令ffmpeg,传入音频文件名即可
    with open(filePath + ".pcm", 'rb') as fp:
        return fp.read()
    

# 创建PyAudio对象
p = pyaudio.PyAudio()


# 打开数据流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

# 开始录音
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

# 停止数据流
stream.stop_stream()
stream.close()

# 关闭PyAudio
p.terminate()

# 写入录音文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# 识别本地文件
a = client.asr(get_file_content('C:/Users/pc/Desktop/program_edit/program/audio/output.wav'), 'pcm', 16000, {
    'dev_pid': 1536,
})
print(a)
