import tkinter as tk
from tkinter import messagebox
import os
from gui import gui_main
from gui2 import gui2_main
from gui3 import gui3_main
from gui3_plot import gui3_plot_main
from guiRecord import guiRecord_main

# Placeholder functions for the features
def open_gui():
    gui_main()

def open_gui2():
    gui2_main()

def open_gui3():
    gui3_main()

def open_gui3_plot():
    gui3_plot_main()

def open_guiRecord():
    guiRecord_main()

# Main Application
def main_interface():
    root = tk.Tk()
    root.title("Final Year Project: Unified Interface")
    root.geometry("500x400")

    # Header
    header = tk.Label(root, text="Welcome to SoundWaves Project", font=("Helvetica", 16, "bold"))
    header.pack(pady=20)

    # Buttons to open functionalities
    gui_button = tk.Button(root, text="Open Gui!", command=open_gui, width=20, height=2)
    gui_button.pack(pady=10)

    gui2_button = tk.Button(root, text="Open Gui2!", command=open_gui2, width=20, height=2)
    gui2_button.pack(pady=10)

    gui3_button = tk.Button(root, text="Open Gui3!", command=open_gui3, width=20, height=2)
    gui3_button.pack(pady=10)

    gui3_plot_button = tk.Button(root, text="Open Gui3_plot!", command=open_gui3_plot, width=20, height=2)
    gui3_plot_button.pack(pady=10)

    guiRecord_button = tk.Button(root, text="Open GuiRecord!", command=open_guiRecord, width=20, height=2)
    guiRecord_button.pack(pady=10)

    # Footer
    footer = tk.Label(root, text="Select a feature to explore", font=("Helvetica", 10, "italic"))
    footer.pack(side=tk.BOTTOM, pady=20)

    root.mainloop()

# Run the main interface
main_interface()
