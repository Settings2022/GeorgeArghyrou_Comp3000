# See .wav stats
import tkinter as tk
from tkinter import messagebox
import wave
import os
from PIL import Image, ImageTk

# Path to the sounds folder
RECORDINGS_FOLDER = "recordings"

# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = RECORDINGS_FOLDER  # Use the RECORDINGS_FOLDER path to get .wav files
    wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
    return wav_files

# Function to create a tooltip for the instructional text
def create_tooltip(parent_frame, x, y, text):
    """
    Creates a tooltip effect for a given question mark (hover to reveal text).
    """

    def show_instruction(event):
        instruction_label.place(x=x + 50, y=y)  # Show tooltip near the question mark

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
                                 wraplength=1200, justify="left", relief="solid", padx=5, pady=5)

# Function to add multiple images
def add_images(parent_frame):
    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "sigma.jpg", "epiphone.jpg", "washburn.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(800, 100), (1450, 650), (800, 1150), (200, 650), (2550, 650), (3200, 650), (1700, 1150) ]  # Position coordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=880, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Stratocaster:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=1750, y=600)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="The Epiphone Les Paul Studio:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=1695, y=1100)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=930, y=1100)
            
            if filename == "sigma.jpg":
                heading_label = tk.Label(parent_frame, text="A Sigma Parlour guitar:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=240, y=600)  # Position the heading above the image
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)

            if filename == "epiphone.jpg":
                heading_label = tk.Label(parent_frame, text="The Noel Gallagher Epiphone Riviera:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=2490, y=600)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "washburn.jpg":
                heading_label = tk.Label(parent_frame, text="A Washburn Parlour guitar:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=3215, y=600)
                img = img.resize((450, 1000), resample=Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            # Create a label for the image
            img_label = tk.Label(parent_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.place(x=image_positions[i][0], y=image_positions[i][1])  # Position the image
            image_labels.append(img_label)
        else:
            print(f"Warning: {filename} not found in the images folder!")

# Main function to initialize the GUI for analyzing wave files
def gui3_main(parent_frame):
    # Adding instructional text to the right side of the screen
    instruction_text = (
        "\n"
        "Here you can view statistical information about recordings you have made.\n"
        "\n"
        "Select a .wav file from the drop-down menu.\n"
        "\n"
        "Click the 'Analyze Wave File' button to display the information.\n"
    )
    # Add tooltip for instructional text
    create_tooltip(parent_frame, x=2200, y=50, text=instruction_text)

    # Load and display multiple images dynamically
    add_images(parent_frame)

    # Get the list of available .wav files
    wav_files = get_wav_files()
    if not wav_files:
        wav_files = ["No .wav files found"]  # Display a message if no .wav files are available

    # Variable to store the selected file from the dropdown menu
    selected_file = tk.StringVar(parent_frame)
    selected_file.set(wav_files[0])  # Set default value for the dropdown if there are files

    # Create a dropdown menu to select a .wav file
    dropdown_label = tk.Label(parent_frame, text="Select .wav file:", font=("Helvetica", 25, "bold"))
    dropdown_label.pack(pady=10)
    
    file_dropdown = tk.OptionMenu(parent_frame, selected_file, *wav_files)
    menu = parent_frame.nametowidget(file_dropdown.menuname)
    menu.config(font=("Helvetica", 25, "bold"))  # Set font for the dropdown menu
    file_dropdown.config(width=20, height=1, font=("Helvetica", 25, "bold"))
    file_dropdown.pack(pady=10)

    # Function to analyze the selected .wav file
    def analyze_wavefile():
        file_path = selected_file.get()  # Get the selected file from the dropdown
        if file_path == "No .wav files found":
            messagebox.showwarning("No files", "No .wav files found in the directory.")
            return

        try:
            # Open the selected .wav file
            with wave.open(file_path, 'r') as obj:
                # Retrieve audio properties
                num_channels = obj.getnchannels()
                samp_width = obj.getsampwidth()
                frame_rate = obj.getframerate()
                num_frames = obj.getnframes()
                total_time_seconds = num_frames / frame_rate
                total_time_minutes = total_time_seconds / 60

                # Display the information in the labels
                channels_label.config(text=f"Number of channels: {num_channels}", font=("Helvetica", 25, "bold"), fg="green")
                sampwidth_label.config(text=f"Sample width: {samp_width}", font=("Helvetica", 25, "bold"), fg="green")
                framerate_label.config(text=f"Frame rate: {frame_rate}", font=("Helvetica", 25, "bold"), fg="green")
                frames_label.config(text=f"Number of frames: {num_frames}", font=("Helvetica", 25, "bold"), fg="green")
                time_seconds_label.config(text=f"Total time (s): {total_time_seconds:.2f}", font=("Helvetica", 25, "bold"), fg="green")
                time_minutes_label.config(text=f"Total time (min): {total_time_minutes:.2f}", font=("Helvetica", 25, "bold"), fg="green")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

    # Create the analyze button
    analyze_button = tk.Button(parent_frame, text="Analyze Wave File", command=analyze_wavefile, font=("Helvetica", 25, "bold"))
    analyze_button.pack(pady=10)

    # Create labels to display the file properties
    channels_label = tk.Label(parent_frame, text="Number of channels: -", font=("Helvetica", 25, "bold"))
    channels_label.pack(pady=5)

    sampwidth_label = tk.Label(parent_frame, text="Sample width: -", font=("Helvetica", 25, "bold"))
    sampwidth_label.pack(pady=5)

    framerate_label = tk.Label(parent_frame, text="Sample rate: -", font=("Helvetica", 25, "bold"))
    framerate_label.pack(pady=5)

    frames_label = tk.Label(parent_frame, text="Number of frames: -", font=("Helvetica", 25, "bold"))
    frames_label.pack(pady=5)

    time_seconds_label = tk.Label(parent_frame, text="Total time (s): -", font=("Helvetica", 25, "bold"))
    time_seconds_label.pack(pady=5)

    time_minutes_label = tk.Label(parent_frame, text="Total time (min): -", font=("Helvetica", 25, "bold"))
    time_minutes_label.pack(pady=5)
