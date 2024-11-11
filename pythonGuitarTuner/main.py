import numpy as np  # Importing the numpy library for numerical operations
import pyaudio  # Importing the PyAudio library to access the audio stream

# Constants
CHUNK = 4096  # Number of samples per frame
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate in Hz


def get_audio_stream():
    """
        Initializes the audio stream.
        Returns:
            stream: The audio input stream object.
            p: The PyAudio object.
        """
    p = pyaudio.PyAudio()  # create PyAudio object
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # open audio input stream
    return stream, p


def detect_frequency(data):
    """
        Detects the frequency of an audio sample.
        Args:
            data: The audio data as bytes.
        Returns:
            peak_freq: The detected peak frequency in Hertz.
        """
    # Convert audio data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)  # convert byte data to numpy array
    # Perform FFT
    fft_spectrum = np.fft.rfft(audio_data)  # perform real FFT on the audio data
    frequencies = np.fft.rfftfreq(len(audio_data), d=1 / RATE)  # calculate frequency bins
    mean_freq = np.sum(frequencies * np.abs(fft_spectrum)) / np.sum(np.abs(fft_spectrum))  # Calculate mean frequency
    return mean_freq


def main():
    # Main function that initializes the audio stream and continuously detects frequencies
    stream, p = get_audio_stream()  # initialise audio stream

    print("Listening...")  # Print a message indicating that listening has started

    try:
        while True:  # Infinite loop to continuously read audio data and detect frequency
            # Read audio data
            data = stream.read(CHUNK)  # read chunk of audio data
            frequency = detect_frequency(data)  # Detect frequency
            print(f"Frequency detected: {frequency:.2f} Hz")  # print detected frequency
    except KeyboardInterrupt:  # Handle keyboard interrupt (Ctrl+C)
        print("Exiting...")  # print message indicating program is exiting
    finally:
        stream.stop_stream()  # Stop the audio stream
        stream.close()  # Close the audio stream
        p.terminate()  # Terminate the PyAudio object


if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
