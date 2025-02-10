# Low Pass Filter Graph
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import wave
import os
from PIL import Image, ImageTk

# Path to the sounds folder
RECORDINGS_FOLDER = "recordings"

# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = RECORDINGS_FOLDER  # Use the SOUNDS_FOLDER path to get .wav files
    wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
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
        cutoff_frequency = 300  # in Hz

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

    # Adding instructional text to the right side of the screen
    instruction_text = (
        "\n"
        "This page allows you to see a low pass filter graph of a recording saved to the recordings folder.\n"
        "\n"
        "Select a .wav file from the drop down menu.\n"
        "\n"
        "Click the Apply Low-Pass Filter button to display the graph.\n"
        "\n"
        "This shows a graph with the original signal in blue and the low-pass filtered signal in red.\n"
        "\n"
        "The cutoff frequency in the code is currently set to 300 Hz.\n"
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 25), wraplength=500, anchor="w")
    instruction_label.place(x=3000, y=50)  # Position the text on the right side with padding

    # Load and rotate the image from the 'images' folder
    image_path = os.path.join(os.getcwd(), 'images', 'gibson.jpg')
    img = Image.open(image_path)
    
    # Resize the image to fit UI
    img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
    img = img.rotate(360, expand=True)
    
    img_tk = ImageTk.PhotoImage(img)

    # Create a label to display the image
    img_label = tk.Label(parent_frame, image=img_tk)
    img_label.image = img_tk  # Keep a reference so it’s not garbage collected
    img_label.place(x=100, y=100)  # Place image on the left side with some padding

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
    plot_frame = tk.Frame(parent_frame, width=800, height=400, padx=100, pady=50)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(20, 10))

    # Embed the figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
