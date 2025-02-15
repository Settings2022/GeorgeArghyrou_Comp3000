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

# Function to create a tooltip for the instructional text
def create_tooltip(parent_frame, x, y, text):
    """
    Creates a tooltip effect for a given question mark (hover to reveal text).
    """

    def show_instruction(event):
        instruction_label.place(x=x + 50, y=y)  # Show tooltip near the question mark

    def hide_instruction(event):
        instruction_label.place_forget()  # Hide tooltip when moving away

    # Create the question mark label
    question_mark = tk.Label(parent_frame, text="?", font=("Helvetica", 30, "bold"),
                             bg="yellow", relief="solid", width=2)
    question_mark.place(x=x, y=y)  # Position the question mark

    # Bind hover events
    question_mark.bind("<Enter>", show_instruction)
    question_mark.bind("<Leave>", hide_instruction)

    # Instructional text label (Initially hidden)
    instruction_label = tk.Label(parent_frame, text=text, font=("Helvetica", 25, "bold"),
                                 wraplength=1000, justify="left", bg="lightgray",
                                 relief="solid", padx=5, pady=5)

# Function to add multiple images
def add_images(parent_frame):

    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "epiphone.jpg"]  # Add more filenames here
    image_positions = [(250, 100), (1450, 1500), (250, 1150), (3050, 1050)]  # Position coordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"))
                heading_label.place(x=330, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Stratocaster:", font=("Arial", 24, "bold"))
                heading_label.place(x=1750, y=1450)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"))
                heading_label.place(x=350, y=1100)

            if filename == "epiphone.jpg":
                heading_label = tk.Label(parent_frame, text="The Noel Gallagher Epiphone Riviera:", font=("Arial", 24, "bold"))
                heading_label.place(x=3000, y=1000)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            # Create a label for the image
            img_label = tk.Label(parent_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.place(x=image_positions[i][0], y=image_positions[i][1])  # Position the image
            image_labels.append(img_label)
        else:
            print(f"Warning: {filename} not found in the images folder!")

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
        label = tk.Label(root, text="Click a button to start tuning.", font=("Helvetica", 40, "bold"))
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
            "Play the corresponding string on your guitar.\n"
            "\n"
            "The app listens for your sound.\n"
            "\n"
            "The needle will show if you are in tune or not.\n"
            "\n"
            "If the needle is in the middle, you are in tune.\n"
        )
        # Add tooltip for instructional text
        create_tooltip(parent_frame=root, x=2800, y=100, text=instruction_text)

        add_images(parent_frame=root)

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
        self.needle_canvas.delete(self.needle)  # Remove the previous needle
        self.needle = self.needle_canvas.create_oval(new_x - 10, 10, new_x + 30, 50, fill="green")

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
