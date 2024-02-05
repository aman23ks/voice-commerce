import pyaudio
import wave

CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("start recording...")
frames = []
seconds = 3
for i in range(0, int(RATE/CHUNK*seconds)):
    data=stream.read(CHUNK)
    frames.append(data)

print("stop recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("output.wav",'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


from google.cloud import speech

client = speech.SpeechClient.from_service_account_file('key.json')
file_name = 'output.wav'

with open(file_name, 'rb') as f:
    wav_data = f.read()

audio_file = speech.RecognitionAudio(content=wav_data)

config = speech.RecognitionConfig(
    sample_rate_hertz=44100,
    enable_automatic_punctuation=True,
    language_code='hi-IN'
)

response = client.recognize(
    config=config,
    audio=audio_file
)

text = response.results[0].alternatives[0].transcript

import os

from google.cloud import translate_v2
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"key.json"

translate_client = translate_v2.Client()
output = translate_client.translate(text, source_language="hi", target_language="en")
print(output)