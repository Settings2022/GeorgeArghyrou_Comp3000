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

# Constants
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def guiRecord_main(parent_frame):
    # Create a label and entry field for the user to input the recording time
    time_label = tk.Label(parent_frame, text="Enter recording duration in seconds:", font=("Helvetica", 12))
    time_label.pack(pady=10)

    time_entry = tk.Entry(parent_frame, font=("Helvetica", 12))
    time_entry.pack(pady=10)
    time_entry.insert(0, "5")  # Default value is 5 seconds

    # Create a label and entry field for the user to input the filename
    filename_label = tk.Label(parent_frame, text="Enter filename (alphanumeric only):", font=("Helvetica", 12))
    filename_label.pack(pady=10)

    filename_entry = tk.Entry(parent_frame, font=("Helvetica", 12))
    filename_entry.pack(pady=10)

    # Create a button that starts the recording process
    start_button = tk.Button(parent_frame, text="Start Recording", font=("Helvetica", 16), command=lambda: start_recording(parent_frame, time_entry.get(), filename_entry.get()))
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

    # Add the .wav extension to the filename
    output_filename = os.path.join(os.getcwd(), filename_input + ".wav")

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)

    # Set up the plot for waveform display
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(0, 2 * FRAMES_PER_BUFFER, 2)
    line, = ax.plot(x, np.random.rand(FRAMES_PER_BUFFER))
    ax.set_ylim(-32768, 32767)
    ax.set_xlim(0, FRAMES_PER_BUFFER)

    frames = []

    # Data generator for the animation
    def data_gen():
        while True:
            data = np.frombuffer(stream.read(FRAMES_PER_BUFFER), dtype=np.int16)
            frames.append(data)
            yield data

    # Update the plot with new data
    def update(data):
        line.set_ydata(data)
        return line,

    # Set up the animation
    ani = animation.FuncAnimation(fig, update, data_gen, blit=True, interval=50)

    # Display the plot in a non-blocking manner
    plt.show(block=False)

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

    # You can add additional behavior to hide the plot after completion if necessary
    plt.close(fig)
