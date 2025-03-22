# Low Pass Filter Graph
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
import wave
import os
import winsound
import threading
import tempfile
import time
from PIL import Image, ImageTk

# Path to the sounds folder
RECORDINGS_FOLDER = "recordings"

# Function to create a tooltip for the instructional text
def create_tooltip(parent_frame, x, y, text):
    """
    Creates a tooltip effect for a given question mark (hover to reveal text).
    """
    def show_instruction(event):
        instruction_label.place(x=x + 50, y=y)  # Show tooltip near the question mark
        instruction_label.lift()  # Ensure it is displayed on top

    def hide_instruction(event):
        instruction_label.place_forget()  # Hide tooltip when moving away

    # Create the question mark label
    question_mark = tk.Label(parent_frame, text="?", font=("Helvetica", 30, "bold"),
                             bg="yellow", relief="solid", width=2)
    question_mark.place(x=x, y=y)  # Position the question mark

    # Bind hover events
    question_mark.bind("<Enter>", show_instruction)
    question_mark.bind("<Leave>", hide_instruction)

    # Instructional text label (Initially hidden)
    instruction_label = tk.Label(parent_frame, text=text, font=("Helvetica", 30, "bold"), bg="black", fg="yellow",
                                 wraplength=1500, justify="left", relief="solid", padx=5, pady=5)

# Function to add multiple images
def add_images(parent_frame):
    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "lowPassLowE.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(200, 100), (1450, 1600), (200, 1100), (1000, 1600), (3200, 700)]  # position co-ordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=270, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Startocaster:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=1750, y=1550)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=310, y=1050)
            
            if filename == "lowPassLowE.jpg":
                heading_label = tk.Label(parent_frame, text="Low pass filter applied to the low E guitar string sound:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=1005, y=1550)  # Position the heading above the image
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="Epiphone Les Paul Studio:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
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

# play filtered sound function
def play_filtered_sound():
    """ Loads a .wav file, applies a low-pass filter, and plays the filtered sound. """
    file_path = selected_file.get()

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Selected file does not exist.")
        return

    try:
        # Load the waveform data
        with wave.open(file_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            num_frames = wav_file.getnframes()
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            audio_data = wav_file.readframes(num_frames)

        # Convert audio bytes to NumPy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Apply the low-pass filter
        cutoff_freq = 250  # Cutoff frequency in Hz
        filtered_audio = low_pass_filter(audio_array, cutoff_freq, sample_rate)

        # Save the filtered audio as a temporary file
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_wav_path = temp_wav.name
        temp_wav.close()  # Close to allow writing

        with wave.open(temp_wav_path, 'wb') as wav_out:
            wav_out.setnchannels(num_channels)
            wav_out.setsampwidth(sample_width)
            wav_out.setframerate(sample_rate)
            wav_out.writeframes(filtered_audio.astype(np.int16).tobytes())

        # Play the filtered sound in a separate thread
        threading.Thread(target=play_and_cleanup, args=(temp_wav_path,), daemon=True).start()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {e}")

def play_and_cleanup(temp_wav_path):
    """ Plays the filtered sound and deletes the temp file after playback. """
    winsound.PlaySound(temp_wav_path, winsound.SND_FILENAME)
    time.sleep(1)  # Ensure sound has finished playing
    os.remove(temp_wav_path)  # Safely delete the temp file


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
        ax.plot(times, signal, label='Original Signal', alpha=0.8, color="blue")
        ax.plot(times, filtered_signal, label='Filtered Signal (Low-Pass)', alpha=0.8, color="red")

        # **Updated: Add axis labels and title**
        ax.set_xlabel("Time (seconds)", fontsize=20)
        ax.set_ylabel("Amplitude", fontsize=20)
        ax.set_title(f"Original (blue) vs Low-Pass Filtered (red) Signal from file named: {file_path}", fontsize=20, fontweight='bold')

        ax.legend(fontsize=15)
        ax.grid()
        canvas.draw()
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")

# Main GUI function
def low_pass_filter_main(parent_frame):

    # Adding instructional text to the right side of the screen
    instruction_text = (
        "This page allows you to see a low pass filter graph of a recording saved to the recordings folder.\n"
        "\n"
        "Useful for removing unwanted high frequency noise or interference, producing a smoother waveform.\n"
        "\n"
        "Demonstrates how filtering affects sound quality and timbre.\n"
        "\n"
        "This shows a graph with the original signal in blue and the low-pass filtered signal in red.\n"
        "\n"
        "Used in audio systems like amplifiers and mixers, allowing users to control the frequency range of the output.\n"
        "\n"
        "The cutoff frequency in the code is currently set to 250 Hz."
    )
    # Add tooltip for instructional text
    create_tooltip(parent_frame, x=2200, y=50, text=instruction_text)

    add_images(parent_frame)

    global selected_file, canvas, fig, ax

    # Get the list of available .wav files
    wav_files = get_wav_files()
    if not wav_files:
        wav_files = ["No .wav files found"]

    selected_file = tk.StringVar(parent_frame)
    selected_file.set(wav_files[0])

    # Dropdown to select .wav file
    tk.Label(parent_frame, text="Select .wav file:", font=("Helvetica", 30, "bold"), bg="black", fg="yellow").pack(pady=5)
    file_dropdown = tk.OptionMenu(parent_frame, selected_file, *wav_files)
    menu = parent_frame.nametowidget(file_dropdown.menuname)
    menu.config(font=("Helvetica", 30, "bold"))
    file_dropdown.config(width=20, height=2, font=("Helvetica", 30, "bold"))
    file_dropdown.pack(pady=5)

    # Button to apply low-pass filter and display waveform
    filter_button = tk.Button(parent_frame, text="Apply Low-Pass Filter", command=display_filtered_waveform, width=25, height=2, font=("Helvetica", 25, "bold"))
    filter_button.pack(pady=20)

    # Button to play the selected sound
    play_button = tk.Button(parent_frame, text="Play Sound", command=play_filtered_sound, width=25, height=2, font=("Helvetica", 25, "bold"))
    play_button.pack(pady=5)

    # Plot frame and matplotlib figure
    plot_frame = tk.Frame(parent_frame, width=600, height=300)
    plot_frame.pack(pady=(20, 20))
    fig, ax = plt.subplots(figsize=(20, 10))

    # **Updated: Set axis labels and title when initializing the figure**
    ax.set_xlabel("Time (seconds)", fontsize=20)
    ax.set_ylabel("Amplitude", fontsize=20)
    ax.set_title("Original (blue) vs Low-Pass Filtered (red) Signal", fontsize=20, fontweight='bold')

    # Embed the figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
