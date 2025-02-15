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

guiRecord.py recordings save to dedicated folder, and graphs removed.

files now play sounds from 'recordings' folder.

Image and text enhancements added to gui.py and guiRecord.
Also gui.py duration changed from ms to s.

Image and text instructions added to all tab interfaces.

Bug - instrument_tab.py crashes when a sound is played.

Actual ukulele string sounds added to sounds folder.
Crash persists.

Loop removed from instrument_tab.py, crash persists when sound is played.

Crash issue resolved by using winsound library instead of simpleaudio.
Repeat look added to instrument_tab.py with stop button.
Feedback provided to tell user which string is being played.

Redundant function def display_waveform_from_file(): removed from gui2.py,
because play_sound_and_plot_from_file(): handles both play and plot.

instrument_tab.py enhancements added

Code added for multiple images on UIs.
Axis labels & title added to low pass filter .py

instrument_tab.py HCI improved: 
Buttons repositioned and enlarged,
but may have too many pics.

autoTune.py HCI improved - images need to be added.

autoTune.py tuning needle changed to oval shape when activated
Images added to autoTune.py.

Title headings added to autoTune, and instrument_tab.

Box shadows added to autoTune and instrument_tab.
Background colour added to all UIs.
Images placed nicely.

gui3.py see wave stats fields & buttons resized.

gui3_plot combo_box options font size increased.
Image corrected for gui2.

Tooltip function added to gui.py, and guy2.py PASS.
 
Tooltips function added to gui3.py PASS.

Tooltips function added to gui3_plot.py PASS.

Tooltips added to guiRecord and lowPassFilter PASS.

Tooltips added to Tune By Ear Instrument_tab PASS.






