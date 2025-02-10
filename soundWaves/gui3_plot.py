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

# Function to add multiple images
def add_images(parent_frame):
    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "sigma.jpg", "epiphone.jpg", "washburn.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(100, 100), (1300, 650), (100, 1050), (700, 650), (2350, 650), (3050, 650), (1500, 1150) ]  # Position coordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"))
                heading_label.place(x=100, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Stratocaster:", font=("Arial", 24, "bold"))
                heading_label.place(x=1300, y=600)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="The Epiphone Les Paul Studio:", font=("Arial", 24, "bold"))
                heading_label.place(x=1500, y=1100)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"))
                heading_label.place(x=100, y=1000)
            
            if filename == "sigma.jpg":
                heading_label = tk.Label(parent_frame, text="A Sigma Parlour guitar:", font=("Arial", 24, "bold"))
                heading_label.place(x=700, y=600)  # Position the heading above the image
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)

            if filename == "epiphone.jpg":
                heading_label = tk.Label(parent_frame, text="The Noel Gallagher Epiphone Riviera:", font=("Arial", 24, "bold"))
                heading_label.place(x=2350, y=600)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "washburn.jpg":
                heading_label = tk.Label(parent_frame, text="A Washburn Parlour guitar:", font=("Arial", 24, "bold"))
                heading_label.place(x=3050, y=600)
                img = img.resize((450, 1000), resample=Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            # Create a label for the image
            img_label = tk.Label(parent_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.place(x=image_positions[i][0], y=image_positions[i][1])  # Position the image
            image_labels.append(img_label)
        else:
            print(f"Warning: {filename} not found in the images folder!")

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

    add_images(parent_frame)  # Add images to the GUI

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

