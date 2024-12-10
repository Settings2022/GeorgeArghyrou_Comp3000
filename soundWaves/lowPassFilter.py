import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import wave
import os

# Function to get all .wav files in the current directory
def get_wav_files():
    folder_path = "."  # Use the current directory
    wav_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    return wav_files

# Design a low-pass filter
def low_pass_filter(data, cutoff_freq, sampling_rate):
    nyquist = sampling_rate / 2
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(6, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Function to load the WAV file
def load_waveform(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_samples = wav_file.getnframes()
        signal = np.frombuffer(wav_file.readframes(num_samples), dtype=np.int16)
    return signal, sample_rate, num_samples

# Function to display the original and filtered waveform
def display_filtered_waveform():
    global ax
    file_path = selected_file.get()

    try:
        signal, sample_rate, num_samples = load_waveform(file_path)
        cutoff_frequency = 150  # in Hz

        # Apply the low-pass filter
        filtered_signal = low_pass_filter(signal, cutoff_frequency, sample_rate)

        # Plot the original and filtered signals
        times = np.linspace(0, num_samples / sample_rate, num_samples)

        ax.clear()
        ax.plot(times, signal, label='Original Signal', alpha=0.7)
        ax.plot(times, filtered_signal, label='Filtered Signal', alpha=0.7, color='red')
        ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Original vs Low-Pass Filtered Signal\n{file_path}')
        ax.legend()
        ax.grid()
        canvas.draw()
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")

# Main GUI function
def low_pass_filter_main(parent_frame):
    global selected_file, canvas, fig, ax

    # Get the list of available .wav files
    wav_files = get_wav_files()
    if not wav_files:
        wav_files = ["No .wav files found"]

    selected_file = tk.StringVar(parent_frame)
    selected_file.set(wav_files[0])

    # Dropdown to select .wav file
    tk.Label(parent_frame, text="Select .wav file:", font=("Helvetica", 20)).pack(pady=5)
    file_dropdown = tk.OptionMenu(parent_frame, selected_file, *wav_files)
    file_dropdown.config(width=20, height=2, font=("Helvetica", 20))
    file_dropdown.pack(pady=5)

    # Button to apply low-pass filter and display waveform
    filter_button = tk.Button(parent_frame, text="Apply Low-Pass Filter", command=display_filtered_waveform, width=25, height=2, font=("Helvetica", 20))
    filter_button.pack(pady=20)

    # Plot frame and matplotlib figure
    plot_frame = tk.Frame(parent_frame)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(20, 10))

    # Embed the figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
