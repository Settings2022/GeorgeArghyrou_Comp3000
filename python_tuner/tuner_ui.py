import tkinter as tk
"""
This module provides a simple GUI-based guitar tuner using Tkinter and PyAudio.
Functions:
    start_tuning(): Captures audio input, processes it to determine the frequency,
                    and provides tuning advice based on the closest guitar string frequency.
UI Elements:
    root: The main Tkinter window.
    detected_freq: StringVar to display the detected frequency.
    string_name: StringVar to display the closest guitar string.
    tuning_advice: StringVar to display tuning advice.
    label_status: Label to display the current status of the tuning process.
Constants:
    FORMAT: Audio format for PyAudio.
    CHANNELS: Number of audio channels.
    RATE: Sampling rate for audio input.
    CHUNK: Number of frames per buffer.
    guitar_frequencies: Dictionary mapping guitar string names to their respective frequencies.
"""
import tkinter as tk
from tkinter import ttk
import pyaudio
import numpy as np
from scipy.fft import fft

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Guitar string frequencies
guitar_frequencies = {
    'E2': 82.41,
    'A2': 110.00,
    'D3': 146.83,
    'G3': 196.00,
    'B3': 246.94,
    'E4': 329.63
}

# Variables for UI and loop control
is_running = False

# Function to start tuning
def start_tuning():
    global is_running
    is_running = True
    label_status.config(text="Recording...")
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    def update_frequency():
        if not is_running:
            # Stop the stream and exit the function if stopped
            stream.stop_stream()
            stream.close()
            audio.terminate()
            label_status.config(text="Tuning stopped.")
            return

        # Capture and process audio data in chunks
        data = stream.read(CHUNK)
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
        detected_freq.set(f"{freq:.2f} Hz")
        string_name.set(closest_string)
        target_freq = guitar_frequencies[closest_string]

        # Provide tuning advice
        if freq < target_freq:
            tuning_advice.set("Tune up")
        elif freq > target_freq:
            tuning_advice.set("Tune down")
        else:
            tuning_advice.set("In tune")
        
        # Schedule the function to run again after a short delay
        root.after(100, update_frequency)

    # Start updating the frequency continuously
    update_frequency()

# Function to stop tuning
def stop_tuning():
    global is_running
    is_running = False

# Setting up the UI
root = tk.Tk()
root.title("Guitar Tuner")

# UI Variables
detected_freq = tk.StringVar()
string_name = tk.StringVar()
tuning_advice = tk.StringVar()

# UI Layout
ttk.Label(root, text="Guitar Tuner", font=("Helvetica", 16)).pack(pady=10)
ttk.Button(root, text="Start Tuning", command=start_tuning).pack(pady=10)
ttk.Button(root, text="Stop Tuning", command=stop_tuning).pack(pady=5)

ttk.Label(root, text="Detected Frequency:").pack()
ttk.Label(root, textvariable=detected_freq, font=("Helvetica", 14)).pack()

ttk.Label(root, text="Closest Guitar String:").pack()
ttk.Label(root, textvariable=string_name, font=("Helvetica", 14)).pack()

ttk.Label(root, text="Tuning Advice:").pack()
ttk.Label(root, textvariable=tuning_advice, font=("Helvetica", 14)).pack()

label_status = ttk.Label(root, text="")
label_status.pack(pady=10)

# Run the application
root.mainloop()

