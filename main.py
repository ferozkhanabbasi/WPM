from subprocess import run, PIPE
import logging
import speech_recognition as sr
import wave
import contextlib
from flask import logging, Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
	filename = "audio.wav"
	r=sr.Recognizer()
	with sr.AudioFile(filename) as source:
		audio_data = r.record(source)
		text = r.recognize_google(audio_data)
	with contextlib.closing(wave.open(filename,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)

	res = len(text.split())/duration #!pip install gTTS pyttsx3 playsound
	res = res*60
	data="words per minutes are "+ str(res)
	return render_template('upload.html',wpm=' Prediction {}'.format(data))
	#return "Total Wpm are" + data


@app.route('/audio', methods=['POST'])
def audio():
    with open('audio.wav', 'wb') as f:
        f.write(request.data)
    proc = run(['ffprobe', '-of', 'default=noprint_wrappers=1', '/audio.wav'], text=True, stderr=PIPE)
    return proc.stderr

@app.route('/read')
def read():
    file= "audio.wav"


@app.route('/aud')
def aud():
    import pyaudio
    import wave
 
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
 
    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")
 
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    



if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port='5001')
