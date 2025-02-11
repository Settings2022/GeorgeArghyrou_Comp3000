import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import threading
from PIL import Image, ImageTk  # Import Pillow for image handling
import pyaudio
from queue import Queue
from scipy.io import wavfile

# Constants
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SOUNDS_FOLDER = "sounds"  # Path to the folder containing string recordings


def load_strums():
    """
    Load the recordings from the 'sounds' folder.
    Returns:
        dict: A dictionary mapping string names to their detected frequencies.
    """
    strums = {}
    for file in os.listdir(SOUNDS_FOLDER):
        if file.endswith(".wav"):
            string_name = os.path.splitext(file)[0]  # get filename without extension
            filepath = os.path.join(SOUNDS_FOLDER, file) # get full path to file
            sample_rate, audio_data = wavfile.read(filepath) # read the audio file
            
            # Perform FFT to find the dominant frequency
            fft_spectrum = np.fft.rfft(audio_data) # Real FFT
            frequencies = np.fft.rfftfreq(len(audio_data), d=1 / sample_rate) # Frequency bins
            dominant_freq = frequencies[np.argmax(np.abs(fft_spectrum))] # Find the dominant frequency
            
            strums[string_name] = dominant_freq # Add to dictionary
    print("Loaded Frequencies:", strums)  # Debugging output to verify frequencies
    return strums


class GuitarTunerApp:
    def __init__(self, root):
        self.root = root
        self.running = True
        self.queue = Queue()
        self.active_string = None  # Active string being tuned

        # GUI Setup
        label = tk.Label(root, text="Click a string button to start tuning.", font=("Helvetica", 20))
        label.pack(pady=10)

        # Define button style
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 18), padding=15)


        # Adding instructional text to the right side of the screen
        instruction_text = (
            "This page allows you to tune your guitar in standard tuning.\n"
            "\n"
            "Select a string by clicking one of the buttons.\n"
            "\n"
            " 1 is the low E string, that's the thickest one on your guitar.\n"
            "\n"
            "2 is the A string, 3 is the D string, 4 is the G string,\n"
            "\n"
            "5 is the B string, and 6 is the high E string.\n"
            "\n"
            "Play the corresponding string on your guitar.\n"
            "\n"
            "The app listens for your sound.\n"
            "\n"
            "The needle will show if you are in tune or not.\n"
            "\n"
            "If the needle is in the middle, you are in tune.\n"
        )
        instruction_label = tk.Label(root, text=instruction_text, font=("Helvetica", 25), wraplength=500, anchor="w")
        instruction_label.place(x=3000, y=50)  # Position the text on the right side with padding

        # Create a frame to hold both guitar and ukulele sections
        instrument_container = ttk.Frame(root)
        instrument_container.pack(pady=10)

        # Guitar Section
        guitar_frame = ttk.Frame(instrument_container)
        guitar_frame.grid(row=0, column=0, padx=100)

        # Guitar Headstock Label
        guitar_label = tk.Label(guitar_frame, text="Guitar Headstock", font=("Arial", 20, "bold"))
        guitar_label.pack()

        # Load and display guitar headstock image
        guitar_tuner_path = os.path.join(os.getcwd(), 'images', 'guitarPegs.jpg')
        guitar_tuner_img = Image.open(guitar_tuner_path)
        guitar_tuner_img = guitar_tuner_img.resize((400, 600), resample=Image.Resampling.LANCZOS)
        guitar_tuner_img_tk = ImageTk.PhotoImage(guitar_tuner_img)
        guitar_tuner_label = tk.Label(guitar_frame, image=guitar_tuner_img_tk)
        guitar_tuner_label.image = guitar_tuner_img_tk
        guitar_tuner_label.pack()

        # Ukulele Section
        ukulele_frame = ttk.Frame(instrument_container)
        ukulele_frame.grid(row=0, column=1, padx=100)

        # Ukulele Headstock Label
        ukulele_label = tk.Label(ukulele_frame, text="Ukulele Headstock", font=("Arial", 20, "bold"))
        ukulele_label.pack()

        # Load and display ukulele headstock image
        ukulele_tuner_path = os.path.join(os.getcwd(), 'images', 'ukulelePegs.jpg')
        ukulele_tuner_img = Image.open(ukulele_tuner_path)
        ukulele_tuner_img = ukulele_tuner_img.resize((400, 600), resample=Image.Resampling.LANCZOS)
        ukulele_tuner_img_tk = ImageTk.PhotoImage(ukulele_tuner_img)
        ukulele_tuner_label = tk.Label(ukulele_frame, image=ukulele_tuner_img_tk)
        ukulele_tuner_label.image = ukulele_tuner_img_tk
        ukulele_tuner_label.pack()

        # call load_strums() to get the references from sounds folder
        self.reference_frequencies = load_strums()

        # Create buttons for each string
        self.buttons = {}
        button_frame = ttk.Frame(guitar_frame)  # Place buttons under the guitar image
        button_frame.pack()

        # Guitar Buttons
        guitar_button_frame = ttk.Frame(guitar_frame)
        guitar_button_frame.pack()

        # Map button labels to actual file names
        button_mapping = {
            "E2": "1", "A": "2", "D": "3", "G": "4", "B": "5", "E": "6"
        }

        guitar_positions = [["D", "G"], ["A", "B"], ["E2", "E"]]

        for row, pair in enumerate(guitar_positions):
            for col, string_name in enumerate(pair):
                mapped_string = button_mapping[string_name]  # Convert label to correct key
                button = ttk.Button(guitar_button_frame, text=string_name, width=20, style="Large.TButton",
                                    command=lambda s=mapped_string: self.activate_string(s))
                button.grid(row=row, column=col, padx=10, pady=5)
                self.buttons[string_name] = button

        # Ukulele Buttons
        ukulele_button_frame = ttk.Frame(ukulele_frame)
        ukulele_button_frame.pack()

        ukulele_positions = [["C", "E"], ["G", "A"]]
        for row, pair in enumerate(ukulele_positions):
            for col, string_name in enumerate(pair):
                button = ttk.Button(ukulele_button_frame, text=string_name, width=20, style="Large.TButton",
                                    command=lambda s=string_name: self.activate_string(s))
                button.grid(row=row, column=col, padx=10, pady=5)
                self.buttons[string_name] = button

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

        # Audio setup
        self.stream, self.p = self.get_audio_stream()
        self.thread = threading.Thread(target=self.update_frequency)
        self.thread.daemon = True
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

    def activate_string(self, string):
        """
        Activate tuning for a specific string.
        """
        self.active_string = string
        # self.feedback_label.config(text=f"Tuning {string}. Play the string.")

        # Reset needle and waveform display
        self.needle_canvas.coords(self.needle, self.needle_center_x, 10, self.needle_center_x, 50)
        self.waveform_canvas.delete("waveform")

    def update_tuning_needle(self, difference, string):
        max_shift = 100
        shift = max_shift * (difference / self.reference_frequencies[string])
        shift = min(max(shift, -max_shift), max_shift)
        new_x = self.needle_center_x + shift
        self.needle_canvas.coords(self.needle, new_x, 10, new_x, 50)

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
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                frequency = self.detect_frequency(audio_data)
                if frequency is not None and self.active_string:
                    self.queue.put((frequency, audio_data))
            except Exception as e:
                print(f"Audio stream error: {e}")

    def process_queue(self):
        if not self.queue.empty() and self.active_string:
            frequency, audio_data = self.queue.get()

            if self.active_string in self.reference_frequencies:
                standard_freq = self.reference_frequencies[self.active_string]
                difference = frequency - standard_freq

                # Update feedback and tuning needle
                if frequency < standard_freq:
                    self.feedback_label.config(text=f"Tune UP to {self.active_string} ({standard_freq:.2f} Hz)")
                elif frequency > standard_freq:
                    self.feedback_label.config(text=f"Tune DOWN to {self.active_string} ({standard_freq:.2f} Hz)")
                else:
                    self.feedback_label.config(text=f"{self.active_string} is in tune!")

                self.update_tuning_needle(difference, self.active_string)
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
