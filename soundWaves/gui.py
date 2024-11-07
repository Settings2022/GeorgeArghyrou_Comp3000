import tkinter as tk
"""
This script creates a Tkinter GUI application that allows users to generate and play a sine wave sound of a specified frequency and duration. 
The waveform of the sound is also plotted in real-time using Matplotlib.
Functions:
    generate_waveform(duration, frequency):
        Generates the time and waveform data for a sine wave based on the given duration and frequency.
    update_plot(i):
        Updates the plot incrementally based on the elapsed time to match the sound duration.
    play_sound_and_plot():
        Retrieves user input for duration and frequency, generates the waveform, plays the sound, and animates the plot.
GUI Elements:
    - Duration entry: Entry widget for the user to input the sound duration in milliseconds.
    - Frequency entry: Entry widget for the user to input the sound frequency in Hz.
    - Frequency label: Label to display the current frequency.
    - Play button: Button to start playing the sound and plotting the waveform.
    - Plot frame: Frame to hold the Matplotlib plot.
    - Canvas: Matplotlib canvas embedded in the Tkinter window to display the animated plot.
"""
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound
import threading
from matplotlib.animation import FuncAnimation
import time



def generate_waveform(duration, frequency):
    # Generate the time and waveform data for a sine wave
    sample_rate = 44100  # Samples per second
    t = np.linspace(0, duration / 1000, int(sample_rate * duration / 1000), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    return t, waveform

def update_plot(i):
    # Stop updating the plot when elapsed time reaches duration
    elapsed_time = time.time() - start_time
    if elapsed_time * 1000 >= duration:
        ani.event_source.stop()  # Stop animation when sound duration has elapsed
        return

    # Plot incrementally based on elapsed time
    end_index = int((elapsed_time * 44100) / 1000)  # Calculate index based on elapsed time
    ax.clear()
    ax.plot(t[:end_index], waveform[:end_index], color="blue")
    ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Sound Waveform - {frequency} Hz')
    ax.grid()

def play_sound_and_plot():
    global t, waveform, frequency, ani, start_time, duration
    
    try:
        duration = int(duration_entry.get())  # Sound duration in milliseconds
        frequency = float(frequency_entry.get())  # Frequency in Hz

        # Generate waveform and display frequency label
        t, waveform = generate_waveform(duration, frequency)
        frequency_label.config(text=f"Frequency: {frequency} Hz")

        # Record start time and play sound in a separate thread
        start_time = time.time()
        threading.Thread(target=lambda: winsound.Beep(int(frequency), duration)).start()

        # Animate plot to match sound duration exactly
        ani = FuncAnimation(fig, update_plot, interval=20, repeat=False)

        # Embed the animated plot in the Tkinter window
        canvas.draw()

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid integers for the duration and frequency.")

# Create the main window
root = tk.Tk()
root.geometry("4000x3200")  # Set the window size to 1200x800 pixels
root.title("Sound Player")

# Create and place the duration entry
tk.Label(root, text="Enter duration (ms):", font=("Helvetica", 50)).pack(pady=5)
duration_entry = tk.Entry(root, font=("Helvetica", 50), width=10)
duration_entry = tk.Entry(root)
duration_entry.pack(pady=5)
duration_entry.config(font=("Helvetica", 50), width=20)

# Create and place the frequency entry
tk.Label(root, text="Enter frequency (Hz):", font=("Helvetica", 50)).pack(pady=5)
frequency_entry = tk.Entry(root, font=("Helvetica", 50), width=10)
frequency_entry.pack(pady=5)
frequency_entry.config(font=("Helvetica", 50), width=20)

# Display the frequency label
frequency_label = tk.Label(root, text="Frequency: - Hz")
frequency_label = tk.Label(root, text="Frequency: - Hz", font=("Helvetica", 50))
frequency_label.pack(pady=5)

# Create and place the play button
play_button = tk.Button(root, text="Play Sound", command=play_sound_and_plot, width=10, height=2, font=("Helvetica", 50))
play_button.pack(pady=30)

# Create a frame to hold the plot and set up the figure and axis
plot_frame = tk.Frame(root)
plot_frame.pack(pady=20)
fig, ax = plt.subplots(figsize=(5, 3))

# Embed the figure in the Tkinter canvas
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().config(width=1000, height=800)  # Set the canvas size
canvas.get_tk_widget().pack()

# Run the application
root.mainloop()
