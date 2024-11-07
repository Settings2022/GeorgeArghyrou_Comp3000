from os import times
import wave
import numpy as np
import matplotlib.pyplot as plt

"""
This script reads a WAV file, extracts its audio signal, and plots the waveform.
Functions:
    None
Modules:
    os.times: Provides access to the times function from the os module.
    wave: Provides a convenient interface to the WAV sound format.
    numpy: Provides support for large, multi-dimensional arrays and matrices.
    matplotlib.pyplot: Provides a MATLAB-like plotting framework.
Variables:
    obj: Wave_read object for reading the WAV file.
    sample_freq: Sampling frequency of the WAV file.
    num_samples: Number of audio frames in the WAV file.
    signal_wave: Raw audio signal read from the WAV file.
    t_audio: Duration of the audio in seconds.
    signal_array: Audio signal converted to a numpy array.
    times: Array of time values corresponding to the audio signal.
"""

obj = wave.open('testSound.wav','r')

sample_freq = obj.getframerate()
num_samples = obj.getnframes()
signal_wave = obj.readframes(-1)

obj.close()

t_audio = num_samples/sample_freq

print(t_audio)

signal_array = np.frombuffer(signal_wave, dtype=np.int16)

times = np.linspace(0, t_audio, len(signal_array))

plt.figure(figsize=(10, 5))
plt.plot(times, signal_array, color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Sound Waveform')
plt.grid()

plt.show()

