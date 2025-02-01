# COMP3000---Computing-Project
COMP3000 - Computing Project
Supervisor: Dr Vasilios Kelefouras.

Project initiation doc complete.

gui.py plots wave form and allows programmer to set frequency & set time via the UI.
gui2.py does the same
gui3.py prints all parameters in the terminal
gui3_plot.py plots the sound wave form
guiRecord.py records and creates a file using internal mic.

Documentation added to prototype files.

gui2.py updated with added documentation to play UI named file contained in root folder.
gui.py updated with added doc, user can now specify freq & time in UI.

gui2.py works with a dropdown selector displaying all available .wav files in root folder

added guitar tuners in python.
python_tuner
pythonGuitarTuner
both require much refinement.

Key Changes to pythonGuitarTuner:
Tuning Needle:
The needle_canvas shows a green line that represents the tuning needle.
The update_tuning_needle method calculates the shift in the needle position based on how far off 
the detected frequency is from the target frequency, within a limited range for smooth visualization.
Waveform Visualization:
The waveform_canvas is used to display the waveform.
The update_waveform method clears the previous waveform and draws a new one based on the 
current audio data. The audio data is normalized and scaled for a consistent visual effect.

Soundwaves interface created to access each function.

Tabs added to frontPage.py for each gui.
guiRecord.py user can set recording duration in seconds.
guiRecord.py user can enter an alphanumeric filename, saved as .wav
guiRecord.py checks if filename already exists.

soundwaves file UI improved, work needed when dragged to larger screen.
test .jpg image added.

pythonGuitarTuner merged into soundWaves,
instrument_tab.py unresponsive, requires fix
autoTune.py requires fix to change needle_canvas to buttons for each string.

autoTune.py needle_canvas changed to buttons
