# play and display .wav
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound
import threading
from matplotlib.animation import FuncAnimation
import time
import wave
import struct
import os  # for file selection

# Initialize global variables
t = np.array([])
waveform = np.array([])
duration = 0
start_time = 0
ani = None

# Path to the sounds folder
SOUNDS_FOLDER = "sounds"

# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = SOUNDS_FOLDER  # Use the SOUNDS_FOLDER path to get .wav files
    wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
    return wav_files

# Get the list of .wav files
wav_files = get_wav_files()
if not wav_files:
    wav_files = ["No .wav files found"]

def get_selected_file_path():
    return selected_file.get()

def load_waveform(file_path):
    global t, waveform
    with wave.open(file_path, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        num_channels = wav_file.getnchannels()
        waveform = np.zeros(num_frames)
        for i in range(num_frames):
            frame = wav_file.readframes(1)
            if num_channels == 2:
                left, right = struct.unpack('<hh', frame)
                waveform[i] = (left + right) / 2
            else:
                waveform[i] = struct.unpack('<h', frame)[0]
        t = np.linspace(0, num_frames / sample_rate, num_frames, endpoint=False)
    return t, waveform

def display_waveform_from_file():
    try:
        file_path = get_selected_file_path()
        load_waveform(file_path)
        ax.clear()
        ax.plot(t, waveform, color="blue", linewidth=0.5, label='Waveform Line')
        ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Waveform from {file_path}')
        ax.legend()
        ax.grid()
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def play_sound_and_plot_from_file():
    global start_time, ani
    try:
        file_path = get_selected_file_path()
        load_waveform(file_path)
        start_time = time.time()
        threading.Thread(target=lambda: winsound.PlaySound(file_path, winsound.SND_FILENAME)).start()
        ani = FuncAnimation(fig, update_plot, interval=20, repeat=False)
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def update_plot(i):
    global t, waveform
    elapsed_time = time.time() - start_time
    max_time = t[-1]
    if elapsed_time >= max_time:
        ani.event_source.stop()
        return
    end_index = int((elapsed_time / max_time) * len(t))
    ax.clear()
    ax.plot(t[:end_index], waveform[:end_index], color="blue")
    ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Sound Waveform')
    ax.grid()

def gui2_main(parent_frame):
    global selected_file, canvas, fig, ax

    # Set up the GUI inside the parent frame
    selected_file = tk.StringVar(parent_frame)
    selected_file.set(wav_files[0])

    # Dropdown to select .wav file
    tk.Label(parent_frame, text="Select .wav file:", font=("Helvetica", 30)).pack(pady=5)
    file_dropdown = tk.OptionMenu(parent_frame, selected_file, *wav_files)
    file_dropdown.config(width=20, height=2, font=("Helvetica", 20))
    file_dropdown.pack(pady=5)

    # Adjust dropdown menu font
    menu = parent_frame.nametowidget(file_dropdown.menuname)
    menu.config(font=("Helvetica", 20))

    # Play button
    play_button = tk.Button(parent_frame, text="Play Sound", command=play_sound_and_plot_from_file, width=20, height=2, font=("Helvetica", 30))
    play_button.pack(pady=20)

    # Plot frame and matplotlib figure
    plot_frame = tk.Frame(parent_frame, width=800, height=400, padx=100, pady=50)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(20, 10))

    # Embed the figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
