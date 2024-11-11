import pyaudio
"""
This script records audio from the microphone for a specified duration and saves it as a WAV file.
Modules:
    pyaudio: Provides Python bindings for PortAudio, the cross-platform audio I/O library.
    wave: Provides a convenient interface to the WAV sound format.
Constants:
    FRAMES_PER_BUFFER (int): The number of frames per buffer.
    FORMAT (int): The format of the audio stream.
    CHANNELS (int): The number of audio channels.
    RATE (int): The sample rate of the audio stream.
    RECORD_SECONDS (int): The duration of the recording in seconds.
Variables:
    p (pyaudio.PyAudio): An instance of the PyAudio class.
    stream (pyaudio.Stream): The audio stream object.
    frames (list): A list to store the recorded audio frames.
    obj (wave.Wave_write): The wave file object.
Functions:
    None
Usage:
    Run the script to start recording audio from the microphone for the specified duration.
    The recorded audio will be saved as 'filename.wav' in the current directory.
"""
import wave

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)


RECORD_SECONDS = 10
frames = []
for i in range(0, int(RATE / FRAMES_PER_BUFFER * RECORD_SECONDS)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

obj = wave.open('fileName.wav', 'wb')
obj.setnchannels(CHANNELS)
obj.setsampwidth(p.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b''.join(frames))
obj.close()
