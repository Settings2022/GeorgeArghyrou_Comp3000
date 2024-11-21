import tkinter as tk
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

def gui_main():
    def update_plot(i):
        elapsed_time = time.time() - start_time
        if elapsed_time * 1000 >= duration:
            ani.event_source.stop()
            return

        end_index = int((elapsed_time * 44100) / 1000)
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

    # Create a Toplevel window
    gui_window = tk.Toplevel()
    gui_window.geometry("1200x800")  # Adjusted to a reasonable size
    gui_window.title("Sound Player")

    # Create and place the duration entry
    tk.Label(gui_window, text="Enter duration (ms):", font=("Helvetica", 16)).pack(pady=5)
    duration_entry = tk.Entry(gui_window, font=("Helvetica", 16), width=10)
    duration_entry.pack(pady=5)

    # Create and place the frequency entry
    tk.Label(gui_window, text="Enter frequency (Hz):", font=("Helvetica", 16)).pack(pady=5)
    frequency_entry = tk.Entry(gui_window, font=("Helvetica", 16), width=10)
    frequency_entry.pack(pady=5)

    # Display the frequency label
    frequency_label = tk.Label(gui_window, text="Frequency: - Hz", font=("Helvetica", 16))
    frequency_label.pack(pady=5)

    # Create and place the play button
    play_button = tk.Button(gui_window, text="Play Sound", command=play_sound_and_plot, font=("Helvetica", 16))
    play_button.pack(pady=30)

    # Create a frame to hold the plot and set up the figure and axis
    plot_frame = tk.Frame(gui_window)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(5, 3))

    # Embed the figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()

    