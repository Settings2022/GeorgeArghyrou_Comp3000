import tkinter as tk  # Importing the tkinter library for creating GUI
from tkinter import ttk  # Importing ttk module from tkinter for styled widgets
import threading  # Importing threading to run processes in parallel
import numpy as np  # Importing numpy for numerical operations
import pyaudio  # Importing PyAudio to access the audio stream
from queue import Queue

# Constants
CHUNK = 4096  # Number of samples per frame, tried 1024, failed to detect low strings
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate in Hz, tried 4800 but failed to detect E2 and A2

# Standard frequencies for 6-string guitar (E, A, D, G, B, E tuning)
STANDARD_FREQUENCIES = {
    "E2": 82.41,
    "A": 110.00,
    "D": 146.83,
    "G": 196.00,
    "B": 246.94,
    "E": 329.63
}


class GuitarTunerApp:
    def __init__(self, root):
        """
        Initializes the Guitar Tuner application.
        Args:
            root: The Tkinter root window.
        """
        self.root = root
        self.root.title("Python Guitar Tuner")  # setting the window title

        self.labels = {}  # Dictionary to store frequency labels for each string
        for string, freq in STANDARD_FREQUENCIES.items():
            label = ttk.Label(root, text=f"{string}: -- Hz", font=("Times New Roman", 16))
            label.pack(pady=5)  # Pack the label into the root window with padding
            self.labels[string] = label

        self.feedback_label = ttk.Label(root, text="", font=("Times New Roman", 16))
        self.feedback_label.pack(pady=20)

        # initialise status progress bar
        self.status_canvas = tk.Canvas(root, width=400, height=60, bg="white")
        self.status_canvas.create_oval(190, 10, 210, 30, fill="blue")
        self.status_canvas.pack(pady=20)
        self.status_bar = self.status_canvas.create_oval(190, 10, 210, 30, fill="green")

        self.running = True  # Flag to control the update loop
        self.queue = Queue()

        self.stream, self.p = self.get_audio_stream()  # initialise the audio stream
        self.thread = threading.Thread(target=self.update_frequency)  # create thread to update frequencies
        self.thread.start()  # start thread

        self.root.after(100, self.process_queue)

    def get_audio_stream(self):
        """
        Initializes and returns the audio stream and PyAudio object.
        Returns:
            stream: The audio input stream object.
            p = PyAudio object
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # open the audio input
        return stream, p

    def detect_frequency(self, data):
        """
        Detects the frequency of an audio sample using FFT.
        Args:
            data: The audio data as a numpy array.
        Returns:
            peak_freq: The detected peak frequency in Hertz.
        """
        # Apply a Hamming window to the data to reduce spectral leakage
        # .hamming
        # .blackman fails to detect E2
        # .hanning fails to detect E2
        # .kaiser UI loads but is unresponsive
        windowed_data = data * np.hamming(len(data))
        # Zero padding for better FFT resolution
        # Perform FFT on the windowed data
        fft_spectrum = np.fft.rfft(windowed_data)
        frequencies = np.fft.rfftfreq(len(windowed_data), d=1 / RATE)
        # Find the peak frequency
        peak_freq = frequencies[np.argmax(np.abs(fft_spectrum))]

        # Filter out frequencies too high or too low
        if peak_freq < 60 or peak_freq > 400:
            return None
        return peak_freq

        # if peak_freq > 80 and peak_freq < 85:
        #     return peak_freq

    def closest_string(self, frequency):
        """
        Finds the closest standard guitar string frequency to a given frequency.
        Args:
            frequency: The detected frequency in Hertz.
        Returns:
            closest_string: The name of the closest standard guitar string.
        """
        closest_string = None
        min_diff = float('inf')  # Initialize minimum difference to infinity
        for string, standard_freq in STANDARD_FREQUENCIES.items():
            # Calculate absolute difference between detected and standard frequencies
            diff = abs(frequency - standard_freq)
            if diff < min_diff:
                min_diff = diff
                closest_string = string
        return closest_string

    # update the status bar
    def update_status_bar(self, difference, string):
        max_shift = 180
        if string is not None:
            standard_freq = STANDARD_FREQUENCIES[string]
            shift = max_shift * (difference / standard_freq)
            shift = min(max(shift, -max_shift), max_shift)  # Clamp the shift value

            # Get current position of the status bar
            current_coords = self.status_canvas.coords(self.status_bar)
            current_shift = current_coords[0] - 190

            # Calculate the step for smooth transition
            step = (shift - current_shift) / 10

            # Update the status bar position gradually
            for i in range(10):
                new_shift = current_shift + step * (i + 1)
                self.status_canvas.coords(self.status_bar, 190 + new_shift, 0, 220 + new_shift, 30)
                self.root.update_idletasks()
                self.root.after(10)
        else:
            self.status_canvas.coords(self.status_bar, 190, 0, 220, 30)  # Reset to center

    def update_frequency(self):
        # Continuously reads audio data, detects frequency, and puts it in the queue
        while self.running:
            data = self.stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            frequency = self.detect_frequency(audio_data)
            if frequency is not None:
                self.queue.put(frequency)  # Put the detected frequency in the queue

    def process_queue(self):
        while not self.queue.empty():
            frequency = self.queue.get()
            closest_string = self.closest_string(frequency)
            for string in STANDARD_FREQUENCIES.keys():
                if string == closest_string:
                    self.labels[string].config(text=f"{string}: {frequency:.2f} Hz")
                    standard_freq = STANDARD_FREQUENCIES[string]
                    if frequency < standard_freq:
                        self.feedback_label.config(text=f"Tune UP to {string} ({standard_freq:.2f} Hz)")
                    elif frequency > standard_freq:
                        self.feedback_label.config(text=f"Tune DOWN to {string} ({standard_freq:.2f} Hz)")
                    else:
                        self.feedback_label.config(text=f"{string} is in tune!")
                else:
                    self.labels[string].config(text=f"{string}: -- Hz")

            for string in STANDARD_FREQUENCIES.keys():
                if string == closest_string:
                    self.labels[string].config(text=f"{string}: {frequency:.2f} Hz")
                    standard_freq = STANDARD_FREQUENCIES[string]
                    difference = frequency - standard_freq
                    self.update_status_bar(difference, string)
                else:
                    self.labels[string].config(text=f"{string}: -- Hz")

        self.root.after(100, self.process_queue)

    def on_close(self):
        # handle the app's closure
        self.running = False  # Stop the update loop
        self.stream.stop_stream()  # Stop the audio stream
        self.stream.close()  # Close the audio stream
        self.p.terminate()  # Terminate the PyAudio object
        self.root.destroy()  # Destroy the root window


if __name__ == "__main__":
    root = tk.Tk()  # Create a Tkinter root window
    app = GuitarTunerApp(root)  # Instantiate the GuitarTunerApp with the root window
    root.protocol("WM_DELETE_WINDOW", app.on_close)  # Set the window close protocol to run on_close method
    root.mainloop()  # Start the Tkinter event loop

