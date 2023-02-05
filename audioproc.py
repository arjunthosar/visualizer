import numpy as np
import pyaudio
import serial
from scipy.fftpack import fft
from time import *
import pystray

# Set the parameters for the audio input
chunkSize = 1024
audioFormat = pyaudio.paInt16
channels = 1
rate = 44100

# Set the number of frequency bands
nBands = 32

# Initialize the lower and upper frequency bounds for the bands
lowerBound = 400
upperBound = 12000

# Determine the frequency range for each band
bandWidth = (upperBound - lowerBound) / nBands
bandRanges = [[lowerBound + i * bandWidth, lowerBound + (i + 1) * bandWidth] for i in range(nBands)]

# Initialize PyAudio
p = pyaudio.PyAudio()

arduino = serial.Serial("COM3", 9600)

# Open a stream for the audio input
stream = p.open(
    format=audioFormat,
    channels=channels,
    rate=rate,
    input=True,
    frames_per_buffer=chunkSize
)

icon = pystray.Icon('icon')

icon.run()

# Continuously read and process audio data
while True:
    try:
        # Read a chunk of audio data from the input stream
        data = stream.read(chunkSize)
        
        # Convert the audio data to a NumPy array
        audioData = np.frombuffer(data, dtype=np.int16)
        
        # Apply FFT to the audio data
        fftData = np.abs(fft(audioData))
        
        # Initialize an empty list for the band magnitudes
        magnitudes = []
        
        # Iterate through the band ranges
        for i in range(nBands):
            # Get the lower and upper frequency bounds for the current band
            lowerBound = bandRanges[i][0]
            upperBound = bandRanges[i][1]
            
            # Determine the indices of the FFT data that correspond to the current band
            lowerIndex = int(lowerBound * chunkSize / rate)
            upperIndex = int(upperBound * chunkSize / rate)
            
            # Extract the FFT data for the current band
            bandData = fftData[lowerIndex:upperIndex]
            
            # Calculate the magnitude of the current band
            bandMagnitude = np.mean(bandData)
            
            # Append the magnitude to the list of band magnitudes
            magnitudes.append(bandMagnitude)
            
        # Determine the strength of each frequency band
        strengths = [min(int(m / (1800 / 2.5)), 8) for m in magnitudes]
        
        # Print the strengths in a neat list
        strengthString = ""
        for s in strengths:
            strengthString += str(s) + ""
        
        # print(bytes(strengthString, encoding='utf8'))
        arduino.write(bytes(strengthString, encoding='utf8'))
        sleep(0.05)
    except KeyboardInterrupt:
        break

# Close the audio stream
stream.stop_stream()
stream.close()

arduino.close()

# Terminate PyAudio
p.terminate()
