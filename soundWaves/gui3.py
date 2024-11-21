import tkinter as tk
from tkinter import messagebox
import wave
import os

# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = "."  # Use the current directory (or specify a path) to get .wav files
    wav_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    return wav_files

# This will be the main function for gui3 that gets called when the button is clicked
def gui3_main():
    # Create the main window for the third GUI
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Wave File Analyzer")

    # List all .wav files in the current directory (or specified folder)
    wav_files = get_wav_files()
    if not wav_files:
        wav_files = ["No .wav files found"]  # Display a message if no .wav files are available

    # Variable to store the selected file from the dropdown menu
    selected_file = tk.StringVar(root)
    selected_file.set(wav_files[0])  # Set default value for the dropdown if there are files

    # Create a dropdown menu to select a .wav file
    dropdown_label = tk.Label(root, text="Select .wav file:", font=("Helvetica", 16))
    dropdown_label.pack(pady=10)
    
    file_dropdown = tk.OptionMenu(root, selected_file, *wav_files)
    file_dropdown.config(width=30, height=2, font=("Helvetica", 16))
    file_dropdown.pack(pady=10)

    # Create a button to analyze the selected .wav file
    def analyze_wavefile():
        file_path = selected_file.get()  # Get the selected file from the dropdown
        if file_path == "No .wav files found":
            messagebox.showwarning("No files", "No .wav files found in the directory.")
            return

        try:
            # Open the selected .wav file
            obj = wave.open(file_path, 'r')

            # Retrieve and display audio properties
            num_channels = obj.getnchannels()
            samp_width = obj.getsampwidth()
            frame_rate = obj.getframerate()
            num_frames = obj.getnframes()
            total_time_seconds = num_frames / frame_rate
            total_time_minutes = total_time_seconds / 60

            # Create and display the information in the labels
            channels_label.config(text=f"Number of channels: {num_channels}")
            sampwidth_label.config(text=f"Sample width: {samp_width}")
            framerate_label.config(text=f"Frame rate: {frame_rate}")
            frames_label.config(text=f"Number of frames: {num_frames}")
            time_seconds_label.config(text=f"Total time (s): {total_time_seconds:.2f}")
            time_minutes_label.config(text=f"Total time (min): {total_time_minutes:.2f}")

            # Close the file
            obj.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

    # Create the analyze button
    analyze_button = tk.Button(root, text="Analyze Wave File", command=analyze_wavefile, font=("Helvetica", 20))
    analyze_button.pack(pady=20)

    # Create labels to display the file properties
    channels_label = tk.Label(root, text="Number of channels: -", font=("Helvetica", 16))
    channels_label.pack(pady=5)

    sampwidth_label = tk.Label(root, text="Sample width: -", font=("Helvetica", 16))
    sampwidth_label.pack(pady=5)

    framerate_label = tk.Label(root, text="Frame rate: -", font=("Helvetica", 16))
    framerate_label.pack(pady=5)

    frames_label = tk.Label(root, text="Number of frames: -", font=("Helvetica", 16))
    frames_label.pack(pady=5)

    time_seconds_label = tk.Label(root, text="Total time (s): -", font=("Helvetica", 16))
    time_seconds_label.pack(pady=5)

    time_minutes_label = tk.Label(root, text="Total time (min): -", font=("Helvetica", 16))
    time_minutes_label.pack(pady=5)

    # Run the main loop of the Tkinter application
    root.mainloop()
