# Plot .wav graph
import os
import wave
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Path to the sounds folder
RECORDINGS_FOLDER = "recordings"

# Function to initialize the waveform plotting GUI
def gui3_plot_main(parent_frame):
    # Create a label for instructions
    label = tk.Label(parent_frame, text="Select a WAV file to plot the waveform", font=("Helvetica", 14))
    label.pack(pady=20)

    # Adding instructional text to the right side of the screen
    instruction_text = (
        "\n"
        "This page allows you to see a graph of a recording saved to the recordings folder.\n"
        "\n"
        "Select a .wav file from the drop down menu.\n"
        "\n"
        "Click the Plot Waveform button to display the graph.\n"
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 25), wraplength=500, anchor="w")
    instruction_label.place(x=3000, y=50)  # Position the text on the right side with padding

    # Load and rotate the image from the 'images' folder
    image_path = os.path.join(os.getcwd(), 'images', 'guitars.jpg')
    img = Image.open(image_path)
    
    # Resize the image to fit your UI
    img = img.resize((600, 900), resample=Image.Resampling.LANCZOS)
    img = img.rotate(360, expand=True)
    
    img_tk = ImageTk.PhotoImage(img)

    # Create a label to display the image
    img_label = tk.Label(parent_frame, image=img_tk)
    img_label.image = img_tk  # Keep a reference so it’s not garbage collected
    img_label.place(x=100, y=100)  # Place image on the left side with some padding

    # List all WAV files in the current directory
    wav_files = [f for f in os.listdir(RECORDINGS_FOLDER) if f.endswith('.wav')] 

    if wav_files:
        # Create a dropdown (Combobox) for selecting a WAV file
        combo_box = ttk.Combobox(parent_frame, values=wav_files, font=("Helvetica", 20), state="readonly")
        combo_box.set("Select WAV File")  # Set default text
        combo_box.pack(pady=20)

        # Create a button to plot the waveform of the selected file
        button = tk.Button(
            parent_frame,
            text="Plot Waveform",
            font=("Helvetica", 20),
            command=lambda: plot_waveform(combo_box.get())
        )
        button.pack(pady=20)
    else:
        # If no WAV files are found in the current directory, show a message
        no_files_label = tk.Label(parent_frame, text="No WAV files found in the current directory.", font=("Helvetica", 20), fg="red")
        no_files_label.pack(pady=20)

# Function to plot the waveform of the selected file
def plot_waveform(selected_file):
    if selected_file == "Select WAV File" or not selected_file:
        return  # Ignore if no valid file is selected

    try:
        # Process the selected WAV file
        file_path = os.path.join(RECORDINGS_FOLDER, selected_file)
        with wave.open(file_path, 'r') as obj:
            sample_freq = obj.getframerate()
            num_samples = obj.getnframes()
            signal_wave = obj.readframes(-1)

        t_audio = num_samples / sample_freq
        signal_array = np.frombuffer(signal_wave, dtype=np.int16)
        times = np.linspace(0, t_audio, len(signal_array))

        # Create the plot for the waveform
        plt.figure(figsize=(20, 10))
        plt.plot(times, signal_array, color='blue')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Sound Waveform')
        plt.grid()

        # Display the plot in a non-blocking way
        plt.show(block=False)

    except Exception as e:
        # Handle any errors and display a message if needed
        error_message = f"An error occurred while processing the file: {e}"
        print(error_message)
        tk.messagebox.showerror("Error", error_message)

