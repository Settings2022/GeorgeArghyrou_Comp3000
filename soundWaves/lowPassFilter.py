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

# Function to add multiple images
def add_images(parent_frame):
    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "lowPassWave.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(200, 100), (2050, 1600), (200, 1100), (1000, 1600), (3200, 700)]  # position co-ordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"))
                heading_label.place(x=270, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Startocaster:", font=("Arial", 24, "bold"))
                heading_label.place(x=2300, y=1550)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"))
                heading_label.place(x=310, y=1050)
            
            if filename == "lowPassWave.jpg":
                heading_label = tk.Label(parent_frame, text="Example of orinigal wave in blue vs low pass wave in red:", font=("Arial", 24, "bold"))
                heading_label.place(x=1005, y=1550)  # Position the heading above the image
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="Epiphone Les Paul Studio:", font=("Arial", 24, "bold"))
                heading_label.place(x=3220, y=650)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            # Create a label for the image
            img_label = tk.Label(parent_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.place(x=image_positions[i][0], y=image_positions[i][1])  # Position the image
            image_labels.append(img_label)
        else:
            print(f"Warning: {filename} not found in the images folder!")


# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = RECORDINGS_FOLDER  # Use the RECORDINGS_FOLDER path to get .wav files
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
        cutoff_frequency = 250  # in Hz

        # Apply the low-pass filter
        filtered_signal = low_pass_filter(signal, cutoff_frequency, sample_rate)

        # Plot the original and filtered signals
        times = np.linspace(0, num_samples / sample_rate, num_samples)

        ax.clear()
        ax.plot(times, signal, label='Original Signal', alpha=0.7, color="blue")
        ax.plot(times, filtered_signal, label='Filtered Signal (Low-Pass)', alpha=0.7, color="red")

        # **Updated: Add axis labels and title**
        ax.set_xlabel("Time (seconds)", fontsize=16)
        ax.set_ylabel("Amplitude", fontsize=16)
        ax.set_title(f"Original (blue) vs Low-Pass Filtered (red) Signal from file named: {file_path}", fontsize=18, fontweight='bold')

        ax.legend()
        ax.grid()
        canvas.draw()
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")

# Main GUI function
def low_pass_filter_main(parent_frame):

    # Adding instructional text to the right side of the screen
    instruction_text = (
        "This page allows you to see a low pass filter graph of a recording saved to the recordings folder.\n"
        "Select a .wav file from the drop-down menu.\n"
        "Click the Apply Low-Pass Filter button to display the graph.\n"
        "This shows a graph with the original signal in blue and the low-pass filtered signal in red.\n"
        "The cutoff frequency in the code is currently set to 250 Hz.\n"
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 20, "bold"), wraplength=1500, anchor="w")
    instruction_label.place(x=2200, y=50)  # Position the text on the right side with padding

    add_images(parent_frame)

    global selected_file, canvas, fig, ax

    # Get the list of available .wav files
    wav_files = get_wav_files()
    if not wav_files:
        wav_files = ["No .wav files found"]

    selected_file = tk.StringVar(parent_frame)
    selected_file.set(wav_files[0])

    # Dropdown to select .wav file
    tk.Label(parent_frame, text="Select .wav file:", font=("Helvetica", 25, "bold")).pack(pady=5)
    file_dropdown = tk.OptionMenu(parent_frame, selected_file, *wav_files)
    file_dropdown.config(width=20, height=2, font=("Helvetica", 25, "bold"))
    file_dropdown.pack(pady=5)

    # Button to apply low-pass filter and display waveform
    filter_button = tk.Button(parent_frame, text="Apply Low-Pass Filter", command=display_filtered_waveform, width=25, height=2, font=("Helvetica", 25, "bold"))
    filter_button.pack(pady=20)

    # Plot frame and matplotlib figure
    plot_frame = tk.Frame(parent_frame, width=800, height=400, padx=100, pady=50)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(20, 10))

    # **Updated: Set axis labels and title when initializing the figure**
    ax.set_xlabel("Time (seconds)", fontsize=16)
    ax.set_ylabel("Amplitude", fontsize=16)
    ax.set_title("Original (blue) vs Low-Pass Filtered (red) Signal", fontsize=18, fontweight='bold')

    # Embed the figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
