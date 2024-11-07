import wave
"""
This script reads and prints various properties of a WAV audio file named 'output.wav'.
Functions:
    wave.open(filename, mode) - Opens a WAV file.
    obj.getnchannels() - Returns the number of audio channels.
    obj.getsampwidth() - Returns the sample width in bytes.
    obj.getframerate() - Returns the frame rate (sample rate).
    obj.getnframes() - Returns the number of audio frames.
    obj.getparams() - Returns a namedtuple containing all the above parameters.
    obj.readframes(n) - Reads and returns at most n frames of audio, as a bytes object.
The script prints:
    - Number of channels in the audio file.
    - Sample width in bytes.
    - Frame rate (sample rate) in Hz.
    - Number of frames in the audio file.
    - All parameters of the audio file.
    - Total time of the audio in seconds.
    - Total time of the audio in minutes.
    - Type and length of the frames read from the audio file.
"""

obj = wave.open('output.wav','r')

print( "Number of channels",obj.getnchannels())
print ( "Sample width",obj.getsampwidth())
print ( "Frame rate.",obj.getframerate())
print ( "Number of frames",obj.getnframes())
print ( "parameters:",obj.getparams())
print ( "Total time in seconds",obj.getnframes()/obj.getframerate())
print ( "Total time in minutes",obj.getnframes()/obj.getframerate()/60)

t_audio = obj.getnframes()/obj.getframerate()
print(t_audio)

frames = obj.readframes(-1)
print(type(frames), type(frames[0]))
print(len(frames))

obj.close()


