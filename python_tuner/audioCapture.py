import pyaudio
"""
This script captures audio from the microphone, performs a Fast Fourier Transform (FFT) to detect the dominant frequency,
and compares it to standard guitar string frequencies to determine the closest string and tuning instructions.
Modules:
    - pyaudio: Provides Python bindings for PortAudio, the cross-platform audio I/O library.
    - numpy: A package for scientific computing with Python.
    - scipy.fft: A module for performing Fast Fourier Transforms.
Parameters:
    FORMAT (int): Audio format (pyaudio.paInt16).
    CHANNELS (int): Number of audio channels (1 for mono).
    RATE (int): Sampling rate (44100 Hz).
    CHUNK (int): Number of frames per buffer (1024).
Functions:
    None
Execution:
    1. Initializes PyAudio and opens an audio stream.
    2. Captures 10 seconds of audio data.
    3. Closes the audio stream.
    4. Converts captured audio frames to a single numpy array.
    5. Performs FFT on the audio data to find the dominant frequency.
    6. Compares the detected frequency to standard guitar string frequencies.
    7. Determines the closest guitar string and provides tuning instructions.
Standard Guitar String Frequencies (Hz):
    - E2: 82.41
    - A2: 110.00
    - D3: 146.83
    - G3: 196.00
    - B3: 246.94
    - E4: 329.63
Output:
    - Detected frequency in Hz.
    - Closest guitar string and its frequency in Hz.
    - Tuning instructions ("Tune up", "Tune down", "In tune").
"""
import numpy as np
from scipy.fft import fft

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # Reduced chunk size for more responsive feedback

# Guitar string frequencies (in Hz)
guitar_frequencies = {
    'E2': 82.41,
    'A2': 110.00,
    'D3': 146.83,
    'G3': 196.00,
    'B3': 246.94,
    'E4': 329.63
}

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Tuner is running. Press Ctrl+C to stop.")

try:
    while True:
        # Capture audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Perform FFT
        N = len(audio_data)
        yf = fft(audio_data)
        xf = np.fft.fftfreq(N, 1 / RATE)

        # Find the peak frequency
        idx = np.argmax(np.abs(yf))
        freq = abs(xf[idx])

        # Find the closest string
        closest_string = min(guitar_frequencies, key=lambda k: abs(guitar_frequencies[k] - freq))
        target_freq = guitar_frequencies[closest_string]

        # Display results
        print(f"Detected frequency: {freq:.2f} Hz")
        print(f"Closest string: {closest_string} ({target_freq} Hz)")

        # Provide tuning advice
        if freq < target_freq:
            print("Tune up")
        elif freq > target_freq:
            print("Tune down")
        else:
            print("In tune")

        print("-" * 30)  # Separator for readability

except KeyboardInterrupt:
    # Close stream and terminate PyAudio on interruption
    print("\nTuning stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

