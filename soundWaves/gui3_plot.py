import os
import wave
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def gui3_plot_main():
    # Create a tkinter window
    root = tk.Tk()
    root.title("Sound Waveform Plotter")

    # Create a label for instructions
    label = tk.Label(root, text="Select a WAV file to plot the waveform", font=("Helvetica", 14))
    label.pack(pady=20)

    # List all WAV files in the current directory
    wav_files = [f for f in os.listdir() if f.endswith('.wav')]

    if wav_files:
        # Create a dropdown (Combobox) for selecting a WAV file
        combo_box = ttk.Combobox(root, values=wav_files, font=("Helvetica", 14), state="readonly")
        combo_box.set("Select WAV File")  # Set default text
        combo_box.pack(pady=20)

        # Create a button to plot the waveform of the selected file
        button = tk.Button(root, text="Plot Waveform", font=("Helvetica", 16), command=lambda: plot_waveform(root, combo_box.get()))
        button.pack(pady=20)
    else:
        # If no WAV files are found in the current directory, show a message
        no_files_label = tk.Label(root, text="No WAV files found in the current directory.", font=("Helvetica", 14), fg="red")
        no_files_label.pack(pady=20)

    # Run the tkinter main loop
    root.mainloop()

def plot_waveform(root, selected_file):
    if selected_file:
        # Process the selected WAV file
        obj = wave.open(selected_file, 'r')

        sample_freq = obj.getframerate()
        num_samples = obj.getnframes()
        signal_wave = obj.readframes(-1)

        obj.close()

        t_audio = num_samples / sample_freq

        signal_array = np.frombuffer(signal_wave, dtype=np.int16)

        times = np.linspace(0, t_audio, len(signal_array))

        # Create the plot for the waveform
        plt.figure(figsize=(10, 5))
        plt.plot(times, signal_array, color='blue')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Sound Waveform')
        plt.grid()

        plt.show()

        # After plotting, close the tkinter window
        root.quit()
