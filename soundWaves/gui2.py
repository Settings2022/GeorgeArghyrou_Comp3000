import tkinter as tk
"""
This script creates a Tkinter GUI application that allows users to load, display, and play sound waveforms from .wav files. 
The waveform is plotted using Matplotlib and the sound is played using the winsound module.
Functions:
    load_waveform(file_path):
        Loads waveform data from a .wav file and returns the time and waveform arrays.
    display_waveform_from_file():
        Loads and displays the waveform from the file path specified in the entry widget.
    play_sound_and_plot_from_file():
        Loads the waveform, plays the sound, and animates the plot to match the sound duration.
    update_plot(i):
        Updates the plot incrementally based on the elapsed time since the sound started playing.
Global Variables:
    t (numpy array): Time array for the waveform.
    waveform (numpy array): Amplitude values of the waveform.
    duration (int): Duration of the sound in seconds.
    start_time (float): Start time of the sound playback.
    ani (FuncAnimation): Animation object for updating the plot.
Tkinter Widgets:
    root (Tk): The main window of the application.
    file_path_entry (Entry): Entry widget for the user to input the file path.
    play_button (Button): Button to start playing the sound and plotting the waveform.
    plot_frame (Frame): Frame to hold the plot.
    fig (Figure): Matplotlib figure for plotting the waveform.
    ax (Axes): Matplotlib axes for the figure.
    canvas (FigureCanvasTkAgg): Canvas to embed the Matplotlib figure in the Tkinter window.
"""
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

# Initialize global variables
t = np.array([])
waveform = np.array([])
duration = 0
start_time = 0
ani = None

def load_waveform(file_path):
    global t, waveform
    # Load waveform data from a .wav file
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
        file_path = file_path_entry.get()  # Get the file path from the entry

        # Load waveform from the .wav file
        load_waveform(file_path)
        
        # Plot the waveform using scatter plot
        ax.clear()
        ax.plot(t, waveform, color="blue", linewidth=0.5, label='Waveform Line')
        ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Waveform from {file_path}')
        ax.legend()
        ax.grid()

        # Embed the plot in the Tkinter window
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def play_sound_and_plot_from_file():
    global start_time, ani
    
    try:
        file_path = file_path_entry.get()  # Get the file path from the entry

        # Load waveform from the .wav file
        load_waveform(file_path)

        # Record start time and play sound in a separate thread
        start_time = time.time()
        threading.Thread(target=lambda: winsound.PlaySound(file_path, winsound.SND_FILENAME)).start()

        # Animate plot to match sound duration exactly
        ani = FuncAnimation(fig, update_plot, interval=20, repeat=False)

        # Embed the animated plot in the Tkinter window
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def update_plot(i):
    global t, waveform  # Ensure global variables are used
    # Stop updating the plot when the sound has finished
    elapsed_time = time.time() - start_time
    max_time = t[-1]  # Total duration of the waveform in seconds

    if elapsed_time >= max_time:
        ani.event_source.stop()  # Stop animation when sound duration has elapsed
        return

    # Plot incrementally based on elapsed time
    end_index = int((elapsed_time / max_time) * len(t))
    ax.clear()
    ax.plot(t[:end_index], waveform[:end_index], color="blue")
    ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Sound Waveform')
    ax.grid()

# Create the main window
root = tk.Tk()
root.geometry("2000x1600")  # Set the window size to 1000x800 pixels
root.title("Sound Player")

# Create and place the file path entry
tk.Label(root, text="Enter file path:", font=("Helvetica", 20)).pack(pady=5)
file_path_entry = tk.Entry(root, width=30, font=("Helvetica", 16))
file_path_entry.pack(pady=5)

# Create and place the play button
play_button = tk.Button(root, text="Play Sound", command=play_sound_and_plot_from_file, width=20, height=2, font=("Helvetica", 16))
play_button.pack(pady=20)

# Create a frame to hold the plot and set up the figure and axis
plot_frame = tk.Frame(root)
plot_frame.pack(pady=20)
fig, ax = plt.subplots(figsize=(16, 8))

# Embed the figure in the Tkinter canvas
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

# Run the application
root.mainloop()
