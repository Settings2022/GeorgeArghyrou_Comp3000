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
RECORD_SECONDS = 5  # Default duration of the recording in seconds

def guiRecord_main(parent_frame):
    # Create a button that starts the recording process within the parent frame
    start_button = tk.Button(parent_frame, text="Start Recording", font=("Helvetica", 16), command=lambda: start_recording(parent_frame))
    start_button.pack(pady=20)

def start_recording(parent_frame):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)

    # Set up the plot for waveform display
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(0, 2 * FRAMES_PER_BUFFER, 2)
    line, = ax.plot(x, np.random.rand(FRAMES_PER_BUFFER))
    ax.set_ylim(-32768, 32767)
    ax.set_xlim(0, FRAMES_PER_BUFFER)

    # Generate a unique filename based on the current date and time
    output_filename = os.path.join(os.getcwd(), datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".wav")
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

