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

# Function to create a tooltip for the instructional text
def create_tooltip(parent_frame, x, y, text):
    """
    Creates a tooltip effect for a given question mark (hover to reveal text).
    """

    def show_instruction(event):
        instruction_label.place(x=x + 250, y=y)  # Show tooltip near the question mark

    def hide_instruction(event):
        instruction_label.place_forget()  # Hide tooltip when moving away

    # Create the question mark label
    question_mark = tk.Label(parent_frame, text="?", font=("Helvetica", 30, "bold"),
                             bg="yellow", relief="solid", width=2)
    question_mark.place(x=x + 200, y=y)  # Position the question mark

    # Bind hover events
    question_mark.bind("<Enter>", show_instruction)
    question_mark.bind("<Leave>", hide_instruction)

    # Instructional text label (Initially hidden)
    instruction_label = tk.Label(parent_frame, text=text, font=("Helvetica", 30, "bold"), bg="black", fg="yellow",
                                 wraplength=1000, justify="left", relief="solid", padx=5, pady=5)

# Function to add multiple images
def add_images(parent_frame):
    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "sigma.jpg", "epiphone.jpg", "washburn.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(200, 100), (1450, 500), (200, 1150), (900, 1150), (2415, 1150), (1655, 1050), (3150, 1150) ]  # Position coordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=250, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Stratocaster:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=1750, y=450)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="The Epiphone Les Paul Studio:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=3140, y=1100)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=300, y=1100)
            
            if filename == "sigma.jpg":
                heading_label = tk.Label(parent_frame, text="A Sigma Parlour guitar:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=950, y=1100)  # Position the heading above the image
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)

            if filename == "epiphone.jpg":
                heading_label = tk.Label(parent_frame, text="The Noel Gallagher Epiphone Riviera:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=2370, y=1100)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "washburn.jpg":
                heading_label = tk.Label(parent_frame, text="A Washburn Parlour guitar:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=1665, y=1000)
                img = img.resize((450, 1000), resample=Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            # Create a label for the image
            img_label = tk.Label(parent_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.place(x=image_positions[i][0], y=image_positions[i][1])  # Position the image
            image_labels.append(img_label)
        else:
            print(f"Warning: {filename} not found in the images folder!")

def guiRecord_main(parent_frame):

    # Add instructional text to help guide the user
    instruction_text = (
        "This section allows you to record audio and save it as a .wav file.\n"
        "\n"
        "You can specify the duration and filename of the recording.\n"
        "\n"
        "Once you start the recording, the audio will be captured and saved in the 'recordings' folder.\n"
        "\n"
        "You can listen to your recording and view graphical images by exploring other tabs in the application."
    )
    # Add tooltip for instructional text
    create_tooltip(parent_frame, x=2400, y=250, text=instruction_text)

    add_images(parent_frame)

    # Create a label and entry field for the user to input the recording time
    time_label = tk.Label(parent_frame, text="Enter recording duration in seconds:", font=("Helvetica", 30, "bold"))
    time_label.pack(pady=10)

    time_entry = tk.Entry(parent_frame, font=("Helvetica", 30, "bold"))
    time_entry.pack(pady=10)
    time_entry.insert(0, "5")  # Default value is 5 seconds

    # Create a label and entry field for the user to input the filename
    filename_label = tk.Label(parent_frame, text="Enter alphanumeric filename to store your recording as a .wav file:", font=("Helvetica", 30, "bold"))
    filename_label.pack(pady=10)

    filename_entry = tk.Entry(parent_frame, font=("Helvetica", 30, "bold"))
    filename_entry.pack(pady=10)

    # Create a button that starts the recording process
    start_button = tk.Button(parent_frame, text="Start Recording", font=("Helvetica", 20, "bold"), command=lambda: start_recording(parent_frame, time_entry.get(), filename_entry.get()))
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
