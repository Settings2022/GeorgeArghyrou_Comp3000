# gui.py contains the implementation of the GuitarTunerApp class, which is responsible for creating the GUI application for the guitar tuner.
import tkinter as tk
from tkinter import ttk
import threading
import numpy as np
import pyaudio
from queue import Queue
from scipy.io import wavfile
import os

# Constants
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SOUNDS_FOLDER = "sounds"  # Path to the folder containing string recordings


def load_reference_frequencies():
    """
    Load the reference frequencies from the recordings in the 'sounds' folder.
    Returns:
        dict: A dictionary mapping string names to their detected frequencies.
    """
    reference_frequencies = {}
    for file in os.listdir(SOUNDS_FOLDER):
        if file.endswith(".wav"):
            string_name = os.path.splitext(file)[0]  # Extract the string name (e.g., "E2")
            filepath = os.path.join(SOUNDS_FOLDER, file)
            sample_rate, audio_data = wavfile.read(filepath)
            
            # Perform FFT to find the dominant frequency
            fft_spectrum = np.fft.rfft(audio_data)
            frequencies = np.fft.rfftfreq(len(audio_data), d=1 / sample_rate)
            dominant_freq = frequencies[np.argmax(np.abs(fft_spectrum))]
            
            reference_frequencies[string_name] = dominant_freq
    return reference_frequencies
print(load_reference_frequencies())
# STANDARD_FREQUENCIES
#     "E2": 82.41,
#     "A": 110.00,
#     "D": 146.83,
#     "G": 196.00,
#     "B": 246.94, 
#     "E": 329.63

class GuitarTunerApp:
    def __init__(self, root):
        self.root = root
        
        label = tk.Label(root, text="Play a string to see if it's in tune.", font=("Helvetica", 20))
        label.pack(pady=10)

        label = tk.Label(root, text="The app will tell you to tune up, down, or in tune.", font=("Helvetica", 20))
        label.pack(pady=10)

        # Load reference frequencies
        self.reference_frequencies = load_reference_frequencies()

        self.labels = {}
        for string in self.reference_frequencies.keys():
            label = ttk.Label(root, text=f"{string}: -- Hz", font=("Times New Roman", 16))
            label.pack(pady=5)
            self.labels[string] = label

        # Feedback label for tuning instructions
        self.feedback_label = ttk.Label(root, text="", font=("Times New Roman", 16))
        self.feedback_label.pack(pady=20)

        # Tuning needle canvas
        self.needle_canvas = tk.Canvas(root, width=400, height=60, bg="white")
        self.needle_center_x = 200
        self.needle = self.needle_canvas.create_line(self.needle_center_x, 10, self.needle_center_x, 50, width=4, fill="green")
        self.needle_canvas.pack(pady=20)

        # Waveform canvas
        self.waveform_canvas = tk.Canvas(root, width=400, height=100, bg="black")
        self.waveform_canvas.pack(pady=10)

        self.running = True
        self.queue = Queue()

        self.stream, self.p = self.get_audio_stream()
        self.thread = threading.Thread(target=self.update_frequency)
        self.thread.start()

        self.root.after(100, self.process_queue)

    def get_audio_stream(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        return stream, p

    def detect_frequency(self, data):
        windowed_data = data * np.hamming(len(data))
        fft_spectrum = np.fft.rfft(windowed_data)
        frequencies = np.fft.rfftfreq(len(windowed_data), d=1 / RATE)
        peak_freq = frequencies[np.argmax(np.abs(fft_spectrum))]

        if 60 <= peak_freq <= 400:
            return peak_freq
        return None

    def closest_string(self, frequency):
        closest_string = None
        min_diff = float('inf')
        for string, standard_freq in self.reference_frequencies.items():
            diff = abs(frequency - standard_freq)
            if diff < min_diff:
                min_diff = diff
                closest_string = string
        return closest_string

    def update_tuning_needle(self, difference, string):
        max_shift = 100
        if string:
            shift = max_shift * (difference / self.reference_frequencies[string])
            shift = min(max(shift, -max_shift), max_shift)
            new_x = self.needle_center_x + shift
            self.needle_canvas.coords(self.needle, new_x, 10, new_x, 50)
        else:
            self.needle_canvas.coords(self.needle, self.needle_center_x, 10, self.needle_center_x, 50)

    def update_waveform(self, audio_data):
        self.waveform_canvas.delete("waveform")
        normalized_data = audio_data / max(abs(audio_data)) * 50
        points = []
        for i in range(0, len(normalized_data), int(len(normalized_data) / 400)):
            x = i / (len(normalized_data) / 400)
            y = 50 + normalized_data[i]
            points.append(x)
            points.append(y)
        self.waveform_canvas.create_line(points, fill="cyan", tags="waveform", smooth=True)

    def update_frequency(self):
        while self.running:
            data = self.stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            frequency = self.detect_frequency(audio_data)
            if frequency is not None:
                self.queue.put((frequency, audio_data))

    def process_queue(self):
        while not self.queue.empty():
            frequency, audio_data = self.queue.get()
            closest_string = self.closest_string(frequency)

            for string in self.reference_frequencies.keys():
                if string == closest_string:
                    self.labels[string].config(text=f"{string}: {frequency:.2f} Hz")
                    standard_freq = self.reference_frequencies[string]
                    difference = frequency - standard_freq

                    if frequency < standard_freq:
                        self.feedback_label.config(text=f"Tune UP to {string} ({standard_freq:.2f} Hz)")
                    elif frequency > standard_freq:
                        self.feedback_label.config(text=f"Tune DOWN to {string} ({standard_freq:.2f} Hz)")
                    else:
                        self.feedback_label.config(text=f"{string} is in tune!")
                    
                    self.update_tuning_needle(difference, string)
                else:
                    self.labels[string].config(text=f"{string}: -- Hz")

            self.update_waveform(audio_data)

        self.root.after(100, self.process_queue)

    def on_close(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GuitarTunerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
# In this script, we have created a GUI application that uses the PyAudio library to continuously detect the frequency of audio input from a microphone. 
# The application displays the detected frequencies of the guitar strings and provides feedback on whether the strings need to be tuned up or down.