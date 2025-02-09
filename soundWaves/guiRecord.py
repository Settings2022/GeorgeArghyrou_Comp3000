import pyaudio
import wave
import numpy as np
import os
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import from Pillow library for images

# Constants
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def guiRecord_main(parent_frame):

    # Load and rotate the image from the 'images' folder
    image_path = os.path.join(os.getcwd(), 'images', 'guitars.jpg')
    img = Image.open(image_path)
    
    # Resize the image to fit UI
    img = img.resize((600, 900), resample=Image.Resampling.LANCZOS)
    img = img.rotate(360, expand=True)
    
    img_tk = ImageTk.PhotoImage(img)

    # Create a label to display the image
    img_label = tk.Label(parent_frame, image=img_tk)
    img_label.image = img_tk  # Keep a reference so it’s not garbage collected
    img_label.place(x=100, y=100)  # Place image on the left side with some padding

    # Add instructional text to help guide the user
    instruction_text = (
        "This section allows you to record audio and save it as a .wav file.\n"
        "\n"
        "You can specify the duration and name of the recording.\n"
        "\n"
        "Once you start the recording, the audio will be captured and saved in the 'recordings' folder.\n"
        "\n"
        "You can listen to your recording and view graphical images by exploring other tabs in the application."
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 25), wraplength=500)
    instruction_label.place(x=3000, y=50)  # Position the text on the right side with padding

    # Create a label and entry field for the user to input the recording time
    time_label = tk.Label(parent_frame, text="Enter recording duration in seconds:", font=("Helvetica", 20))
    time_label.pack(pady=10)

    time_entry = tk.Entry(parent_frame, font=("Helvetica", 20))
    time_entry.pack(pady=10)
    time_entry.insert(0, "5")  # Default value is 5 seconds

    # Create a label and entry field for the user to input the filename
    filename_label = tk.Label(parent_frame, text="Enter alphanumeric filename to store your recording as a .wav file:", font=("Helvetica", 20))
    filename_label.pack(pady=10)

    filename_entry = tk.Entry(parent_frame, font=("Helvetica", 20))
    filename_entry.pack(pady=10)

    # Create a button that starts the recording process
    start_button = tk.Button(parent_frame, text="Start Recording", font=("Helvetica", 20), command=lambda: start_recording(parent_frame, time_entry.get(), filename_entry.get()))
    start_button.pack(pady=20)

def start_recording(parent_frame, time_input, filename_input):
    try:
        # Convert the user input to an integer (duration of the recording in seconds)
        RECORD_SECONDS = int(time_input)
        if RECORD_SECONDS <= 0:
            raise ValueError("Duration must be a positive integer.")
    except ValueError:
        # If the user inputs an invalid value, show an error message
        messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the duration.")
        return

    # Validate filename to ensure it only contains alphanumeric characters
    if not filename_input.isalnum():
        messagebox.showerror("Invalid Filename", "Filename must only contain alphanumeric characters (letters and numbers).")
        return

    # If no filename is provided, generate a default one based on the current date and time
    if not filename_input:
        filename_input = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the path to the recordings folder
    recordings_folder = os.path.join(os.getcwd(), 'recordings')
    
    # Ensure the folder exists, create it if necessary
    if not os.path.exists(recordings_folder):
        os.makedirs(recordings_folder)

    # Add the .wav extension to the filename and construct the full path
    output_filename = os.path.join(recordings_folder, filename_input + ".wav")

    # Check if the file already exists
    if os.path.exists(output_filename):
        messagebox.showerror("File Exists", f"The file '{filename_input}.wav' already exists. Please choose a different filename.")
        return

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)

    frames = []

    # Start recording for the specified duration
    start_time = time.time()
    while time.time() - start_time < RECORD_SECONDS:
        data = np.frombuffer(stream.read(FRAMES_PER_BUFFER), dtype=np.int16)
        frames.append(data)

    # Save the recorded frames as a WAV file
    with wave.open(output_filename, 'wb') as obj:
        obj.setnchannels(CHANNELS)
        obj.setsampwidth(p.get_sample_size(FORMAT))
        obj.setframerate(RATE)
        obj.writeframes(b''.join(frames))

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Inform the user that the recording is saved
    messagebox.showinfo("Recording Complete", f"Recording saved as {output_filename}")
