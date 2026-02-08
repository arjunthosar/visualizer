import numpy as np
import pyaudio
import serial
from scipy.fftpack import fft
from time import *
good = True
import msvcrt
import subprocess
from threading import *
import psutil
detected = False

            #TODO: get exec detection to work

# Set the parameters for the audio input
chunkSize = 1024
audioFormat = pyaudio.paInt16
channels = 1
rate = 44100

# Set the number of frequency bands
nBands = 32

# Initialize the lower and upper frequency bounds for the bands
lowerBound = 100
upperBound = 5100

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

def start():
    global good
    good=True
    visualize()
def stop():
    global good
    good=False
    arduino.write(bytes('00000000000000000000000000000000', encoding='utf8'))
    while not msvcrt.kbhit():
        pass
    if msvcrt.getwche() == '\r':
        sleep(0.2)
        start()

def detect_executable(executable_name):
    """Detect if an executable is running, and print 'Detected!' if it is."""
    last_detected = False
    while True:
        detected = any(process.info['name'] == executable_name for process in psutil.process_iter(['name']))
        if detected and not last_detected:
            print('Detected!')
        last_detected = detected
        psutil.wait_procs(psutil.process_iter(['name']), timeout=1)


# options = (("Start", None, start), ("Stop", None, stop))
# icon = SysTrayIcon("music.ico", "Visualizer", options)
# thr=Thread(None, target=icon.start)
# icon.start()

# Continuously read and process audio data
def visualize():
    global good
    print('func')
    try:
        # icon.start()
        while good:
            # thr.run()
            # icon.start()
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
                if i<3:
                    magnitudes.append(bandMagnitude/12)
                elif i<5:
                    magnitudes.append(bandMagnitude/10)
                elif i<9:
                    magnitudes.append(bandMagnitude/5.5)
                elif i<18:
                    magnitudes.append(bandMagnitude/2.5)
                elif i<24:
                    magnitudes.append(bandMagnitude/1.5)
                else:
                    magnitudes.append(bandMagnitude/1)

                # magnitudes.append(bandMagnitude)

            # Determine the strength of each frequency band
            strengths = [min(int(m / (1800 / 4)), 8) for m in magnitudes]
            # strengths = []
            # for m in range(len(magnitudes)):
                # if m<7:
                #     strengths.append([min(int(magnitudes[m] / (1800 / 6)), 8)])
                # else:
                # strengths.append([min(int(magnitudes[m] / (1800 / 2.5)), 8)])
            
            # Print the strengths in a neat list
            strengthString = ""
            for s in strengths:
                strengthString += str(s) + ""
            
            # print(bytes(strengthString, encoding='utf8'))
            arduino.write(bytes(strengthString, encoding='utf8'))
            sleep(0.043)
            if msvcrt.kbhit():
                if msvcrt.getwche() == '\r':
                    stop()
                
    except KeyboardInterrupt:
        # Close the audio stream
        stream.stop_stream()
        stream.close()

        arduino.close()

        # Terminate PyAudio
        p.terminate()
        good=False

t1=Thread(target=visualize)
t2=Thread(target=detect_executable, args=("Code.exe",))

t1.start()
t2.start()