import tkinter as tk
from tkinter import messagebox
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound
import threading
from matplotlib.animation import FuncAnimation
import time
from PIL import Image, ImageTk  # Import Pillow for image handling

# Function to generate waveform
def generate_waveform(duration, frequency):
    sample_rate = 44100  # Samples per second
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    return t, waveform

# Main function to build the GUI
def gui_main(parent_frame):
    # Function to update the plot
    def update_plot(i):
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            ani.event_source.stop()
            return

        end_index = int((elapsed_time * 44100) / 1000)
        ax.clear()  # Clear previous plot

        # Plot the updated waveform
        ax.plot(t[:end_index], waveform[:end_index], color="blue")

        # Add axis labels and title
        ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Sound Waveform - {frequency} Hz')
        ax.grid()

    # Play sound and plot the waveform
    def play_sound_and_plot():
        global t, waveform, frequency, ani, start_time, duration

        try:
            # Get user input for duration and frequency
            duration = float(duration_entry.get())  # Duration in seconds
            frequency = float(frequency_entry.get())  # Frequency in Hz

            # Generate waveform based on input
            t, waveform = generate_waveform(duration, frequency)

            # Update the frequency label to show the current frequency
            frequency_label.config(text=f"Frequency: {frequency} Hz")

            # Record the start time and start the sound in a background thread
            start_time = time.time()

            # Convert duration to milliseconds for winsound.Beep
            winsound_duration = int(duration * 1000)  # Convert seconds to milliseconds
            threading.Thread(target=lambda: winsound.Beep(int(frequency), winsound_duration)).start()

            # Start the animation to update the plot
            ani = FuncAnimation(fig, update_plot, interval=20, repeat=False)

            # Embed the plot in the Tkinter canvas
            canvas.draw()

        except ValueError:
            # Show error if the user enters invalid input
            messagebox.showerror("Invalid input", "Please enter valid integers for the duration and frequency.")

    # Adding instructional text to the right side of the screen
    instruction_text = (
        "\n"
        "This page allows you to generate and play a sound with a specified frequency and duration.\n"
        "\n"
        "You can visualize the waveform of the sound as it plays.\n"
        "\n"
        "Enter the frequency (in Hz).\n"
        "\n"
        "Set the duration (in seconds).\n"
        "\n"
        "To generate a sine wave, click 'Play Sound'."
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 25), wraplength=500, anchor="w")
    instruction_label.place(x=3000, y=50)  # Position the text on the right side with padding

    # Load and rotate the image from the 'images' folder
    image_path = os.path.join(os.getcwd(), 'images', 'gibson.jpg')
    img = Image.open(image_path)
    
    # Resize the image to fit UI
    img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
    img = img.rotate(360, expand=True)
    
    img_tk = ImageTk.PhotoImage(img)

    # Create a label to display the image
    img_label = tk.Label(parent_frame, image=img_tk)
    img_label.image = img_tk  # Keep a reference so it’s not garbage collected
    img_label.place(x=100, y=100)  # Place image on the left side with some padding

    # Create and place the input fields for duration and frequency
    tk.Label(parent_frame, text="Enter duration (s):", font=("Helvetica", 30)).pack(pady=5)
    duration_entry = tk.Entry(parent_frame, font=("Helvetica", 20), width=10)
    duration_entry.pack(pady=5)
    duration_entry.insert(0, "5")  # Default value is 5 seconds

    tk.Label(parent_frame, text="Enter frequency (Hz):", font=("Helvetica", 30)).pack(pady=5)
    frequency_entry = tk.Entry(parent_frame, font=("Helvetica", 16), width=10)
    frequency_entry.pack(pady=5)

    # Display frequency
    frequency_label = tk.Label(parent_frame, text="Frequency: - Hz", font=("Helvetica", 20))
    frequency_label.pack(pady=5)

    # Play sound button
    play_button = tk.Button(parent_frame, text="Play Sound", command=play_sound_and_plot, font=("Helvetica", 20))
    play_button.pack(pady=30)

    # Create a frame for the plot and set up the figure and axis
    plot_frame = tk.Frame(parent_frame, width=800, height=400, padx=100, pady=50)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(20, 10))

    # Add axis labels for the graph
    ax.set_xlabel('Time (seconds)', fontsize=18)
    ax.set_ylabel('Amplitude', fontsize=18)
    ax.set_title('Sound Waveform', fontsize=20)

    # Embed the plot in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
