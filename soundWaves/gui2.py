
import tkinter as tk
"""
This script creates a Tkinter GUI application for playing and visualizing .wav sound files.
It includes functionalities to load .wav files, display their waveforms, and play the sound
while animating the waveform plot.
Functions:
    get_wav_files():
        Retrieves all .wav files in the current directory.
    get_selected_file_path():
        Returns the selected file path from the dropdown menu.
    show_selected_file():
        Prints the selected file path for testing purposes.
    load_waveform(file_path):
        Loads waveform data from a specified .wav file.
    display_waveform_from_file():
        Displays the waveform of the selected .wav file in the plot.
    play_sound_and_plot_from_file():
        Plays the sound of the selected .wav file and animates the waveform plot.
    update_plot(i):
        Updates the plot incrementally based on the elapsed time during sound playback.
Global Variables:
    t (numpy array): Time values for the waveform.
    waveform (numpy array): Amplitude values of the waveform.
    duration (int): Duration of the sound file.
    start_time (float): Start time of the sound playback.
    ani (FuncAnimation): Animation object for updating the plot.
GUI Elements:
    root (Tk): Main window of the application.
    selected_file (StringVar): Variable to store the selected file.
    file_dropdown (OptionMenu): Dropdown menu for file selection.
    play_button (Button): Button to play the sound and animate the plot.
    plot_frame (Frame): Frame to hold the plot.
    fig (Figure): Matplotlib figure for plotting.
    ax (Axes): Matplotlib axes for plotting.
    canvas (FigureCanvasTkAgg): Canvas to embed the plot in the Tkinter window.
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
import os # for file selection

# Initialize global variables
t = np.array([])
waveform = np.array([])
duration = 0
start_time = 0
ani = None

# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = "."  # Use the current directory 'soundWaves'
    wav_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    return wav_files

# Get the list of .wav files
wav_files = get_wav_files()
if not wav_files:
    wav_files = ["No .wav files found"]  # Display a message if no .wav files are available

# Function to get the selected file path from the dropdown menu
def get_selected_file_path():
    return selected_file.get()  # Only returns the selected filename

# Test function to show the selected file
def show_selected_file():
    print("Selected file path:", get_selected_file_path())

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
        file_path = get_selected_file_path()  # Get the file path from the entry

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
        file_path = get_selected_file_path()  # Get the file path from the entry

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

# Variable to store the selected file
selected_file = tk.StringVar(root)
selected_file.set(wav_files[0])  # Set default value for the dropdown

# Create and place the dropdown menu for file selection
tk.Label(root, text="Select .wav file:", font=("Helvetica", 20)).pack(pady=5)
file_dropdown = tk.OptionMenu(root, selected_file, *wav_files,)
file_dropdown.config(width=20, height=2, font=("Helvetica", 20))
file_dropdown.pack(pady=5)

# Configure the dropdown menu to have larger text for the displayed list of files
menu = root.nametowidget(file_dropdown.menuname)
menu.config(font=("Helvetica", 20))

# Create and place the play button
play_button = tk.Button(root, text="Play Sound", command=play_sound_and_plot_from_file, width=20, height=2, font=("Helvetica", 20))
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
