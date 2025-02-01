# See .wav stats
import tkinter as tk
from tkinter import messagebox
import wave
import os

# Path to the sounds folder
RECORDINGS_FOLDER = "recordings"

# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = RECORDINGS_FOLDER  # Use the SOUNDS_FOLDER path to get .wav files
    wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
    return wav_files

# Main function to initialize the GUI for analyzing wave files
def gui3_main(parent_frame):
    # Get the list of available .wav files
    wav_files = get_wav_files()
    if not wav_files:
        wav_files = ["No .wav files found"]  # Display a message if no .wav files are available

    # Variable to store the selected file from the dropdown menu
    selected_file = tk.StringVar(parent_frame)
    selected_file.set(wav_files[0])  # Set default value for the dropdown if there are files

    # Create a dropdown menu to select a .wav file
    dropdown_label = tk.Label(parent_frame, text="Select .wav file:", font=("Helvetica", 20))
    dropdown_label.pack(pady=10)
    
    file_dropdown = tk.OptionMenu(parent_frame, selected_file, *wav_files)
    menu = parent_frame.nametowidget(file_dropdown.menuname)
    menu.config(font=("Helvetica", 20))
    file_dropdown.config(width=30, height=2, font=("Helvetica", 20))
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
                channels_label.config(text=f"Number of channels: {num_channels}", font=("Helvetica", 20))
                sampwidth_label.config(text=f"Sample width: {samp_width}", font=("Helvetica", 20))
                framerate_label.config(text=f"Frame rate: {frame_rate}", font=("Helvetica", 20))
                frames_label.config(text=f"Number of frames: {num_frames}", font=("Helvetica", 20))
                time_seconds_label.config(text=f"Total time (s): {total_time_seconds:.2f}", font=("Helvetica", 20))
                time_minutes_label.config(text=f"Total time (min): {total_time_minutes:.2f}", font=("Helvetica", 20))
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

    # Create the analyze button
    analyze_button = tk.Button(parent_frame, text="Analyze Wave File", command=analyze_wavefile, font=("Helvetica", 20))
    analyze_button.pack(pady=20)

    # Create labels to display the file properties
    channels_label = tk.Label(parent_frame, text="Number of channels: -", font=("Helvetica", 20))
    channels_label.pack(pady=5)

    sampwidth_label = tk.Label(parent_frame, text="Sample width: -", font=("Helvetica", 20))
    sampwidth_label.pack(pady=5)

    framerate_label = tk.Label(parent_frame, text="Frame rate: -", font=("Helvetica", 20))
    framerate_label.pack(pady=5)

    frames_label = tk.Label(parent_frame, text="Number of frames: -", font=("Helvetica", 20))
    frames_label.pack(pady=5)

    time_seconds_label = tk.Label(parent_frame, text="Total time (s): -", font=("Helvetica", 20))
    time_seconds_label.pack(pady=5)

    time_minutes_label = tk.Label(parent_frame, text="Total time (min): -", font=("Helvetica", 20))
    time_minutes_label.pack(pady=5)

