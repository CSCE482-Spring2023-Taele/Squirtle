import wave, struct, math # To calculate the WAV file content
import numpy as np # To handle matrices
import os
from PIL import Image # To open the input image and convert it to grayscale

import scipy.ndimage # To resample using nearest neighbour

class Sonify:
    def __init__(self, directory):
        self.input_dir = directory + "/figures"
        self.output_dir = directory + "/sonify"

    def sonifyPDFImages(self):
        for files in os.listdir(self.input_dir):
            if files[:-3] != 'wav':
                path = os.path.join(self.input_dir, files)
                self.genSoundFromImage(path, os.path.splitext(path)[0] + ".wav")


    def loadPicture(self, size, file, contrast=True, highpass=False, verbose=1):
        img = Image.open(file)
        img = img.convert("L")
        
        imgArr = np.array(img)
        imgArr = np.flip(imgArr, axis=0)
        if verbose:
            print("Image original size: ", imgArr.shape)
            
        # Increase the contrast of the image
        if contrast:
            imgArr = 1/(imgArr+10**15.2) # Now only god knows how this works but it does
        else:
            imgArr = 1 - imgArr

        imgArr -= np.min(imgArr)
        imgArr = imgArr/np.max(imgArr)
        # Remove low pixel values (highpass filter)
        if highpass:
            removeLowValues = np.vectorize(lambda x: x if x > 0.5 else 0, otypes=[float])
            imgArr = removeLowValues(imgArr)

        if size[0] == 0:
            size = imgArr.shape[0], size[1]
        if size[1] == 0:
            size = size[0], imgArr.shape[1]
        resamplingFactor = size[0]/imgArr.shape[0], size[1]/imgArr.shape[1]
        if resamplingFactor[0] == 0:
            resamplingFactor = 1, resamplingFactor[1]
        if resamplingFactor[1] == 0:
            resamplingFactor = resamplingFactor[0], 1
        
        # Order : 0=nearestNeighbour, 1:bilinear, 2:cubic etc...
        imgArr = scipy.ndimage.zoom(imgArr, resamplingFactor, order=0)
        
        if verbose:
            print("Resampling factor", resamplingFactor)
            print("Image resized :", imgArr.shape)
            print("Max intensity: ", np.max(imgArr))
            print("Min intensity: ", np.min(imgArr))
        return imgArr

    def genSoundFromImage(self, file, output="sound.wav", duration=1.0, sampleRate=44100.0, intensityFactor=1, min_freq=0, max_freq=22000, invert=False, contrast=True, highpass=True, verbose=False):
        wavef = wave.open(output,'w')
        wavef.setnchannels(1) # mono
        wavef.setsampwidth(2) 
        wavef.setframerate(sampleRate)
        
        max_frame = int(duration * sampleRate)
        max_intensity = 32767 # Defined by WAV
        
        stepSize = 400 # Hz, each pixel's portion of the spectrum
        steppingSpectrum = int((max_freq-min_freq)/stepSize)
        
        imgMat = self.loadPicture(size=(steppingSpectrum, max_frame), file=file, contrast=contrast, highpass=highpass, verbose=verbose)
        if invert:
            imgMat = 1 - imgMat
        imgMat *= intensityFactor # To lower/increase the image overall intensity
        imgMat *= max_intensity # To scale it to max WAV audio intensity
        if verbose:
            print("Input: ", file)
            print("Duration (in seconds): ", duration)
            print("Sample rate: ", sampleRate)
            print("Computing each soundframe sum value..")
        for frame in range(max_frame):
            if frame % 60 == 0: # Only print once in a while
                print("Progress: ==> {:.2%}".format(frame/max_frame), end="\r")
            signalValue, count = 0, 0
            for step in range(steppingSpectrum):
                intensity = imgMat[step, frame]
                if intensity < 0.1*intensityFactor:
                    continue
                # nextFreq is less than currentFreq
                currentFreq = (step * stepSize) + min_freq
                nextFreq = ((step+1) * stepSize) + min_freq
                if nextFreq - min_freq > max_freq: # If we're at the end of the spectrum
                    nextFreq = max_freq
                for freq in range(currentFreq, nextFreq, 1000): # substep of 1000 Hz is good
                    signalValue += intensity*math.cos(freq * 2 * math.pi * float(frame) / float(sampleRate))
                    count += 1
            if count == 0: count = 1
            signalValue /= count
            
            data = struct.pack('<h', int(signalValue))
            wavef.writeframesraw( data )
            
        wavef.writeframes(''.encode())
        wavef.close()
        print("\nProgress: ==> 100%")
        if verbose:
            print("Output: ", output)

