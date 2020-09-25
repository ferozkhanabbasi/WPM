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



if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port='5005')
