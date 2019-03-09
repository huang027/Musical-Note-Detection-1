"""
FIRST REAL IMPLEMENTATION THAT WASN'T JUST COPY PASTED FROM OTHE INTERNET
This is the implementation of what was gathered from other code. This should
give the frequency of a sound. For the c note tested it registers near a C5.
The percent error of this test is less than 1% if this is not a mere
coincidence.
The webpage below is used to compare frequencies:
http://pages.mtu.edu/~suits/notefreqs.html

UPDATE 3/6/18 2:03PM: THIS ALSO WORKS WITH AN A NOTE!!
We need to get this to work with more than just a single note at a time!

UPDATE 3/8/18 6:00PM: Other notes implemented. Can now return a note value.
Still needs adjustments, F, F# and G would not work.
"""

import wave
import numpy as np

"""
A hash table to store each note.
Each note is the value and the frequency
is the key.
Notes and frequencies came from:
http://pages.mtu.edu/~suits/notefreqs.html
UNFINISHED!
"""
NOTES = {
    '261.63': 'C4', '277.18': 'C#4/Db4',
    '293.66': 'D4', '311.13': 'D#4/Eb4',
    '329.63': 'E4', '349.23': 'F4',
    '369.99': 'F#4/Gb4', '392.00': 'G4',
    '415.30': 'G#4/Ab4', '440.00': 'A4',
    '466.16': 'A#4/Bb4', '493.88': 'B4',
    '523.25': 'C5', '554.37': 'C#5/Db5',
    '587.33': 'D5', '622.25': 'D#5//Eb5',
    '659.25': 'E5', '698.46': 'F5'
}


DEBUGGING = False
def get_frequency(file):
    # this was tested using a chunk of 2048
    # and a chunk of 4096
    # play with this value at will
    chunk = 2048

    wave_file = wave.open(file, 'rb')
    sample_width = wave_file.getsampwidth()
    rate = wave_file.getframerate()
    # had to multiply the chunk by 2 here (1)
    # not sure why or what chunk even means
    window = np.blackman(chunk*2)

    data = wave_file.readframes(chunk)
    if DEBUGGING:
        print(len(data))
        print(2*chunk*sample_width)

    # unpack data and mult by window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/sample_width),\
                                        data))*window
    # take fft and square each element
    fft_data = abs(np.fft.rfft(indata)) ** 2
    # find the max frequency
    max = fft_data[1:].argmax() + 1

    # quadratic interpolation
    if max != len(fft_data)-1:
        y0,y1,y2 = np.log(fft_data[max-1:max+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (max+x1)*rate/chunk
        # print("IN IF")
        return thefreq
    else:
        thefreq = max*rate/chunk
        # print("IN ELSE")
        return thefreq

"""
This function uses the hash table to get the frequencies. This makes more sense
as opposed to manually checking everything.
"""
def get_note(frequency):
    # loops through the hash table
    for key in NOTES:
        # calculates the percent error
        percent_error = ((frequency - float(key)) / float(key)) * 100
        # gets the absolute value so no negatives
        percent_error = abs(percent_error)
        # checks if percent error is less than 1
        if percent_error < 1.3:
            calc_note = NOTES[key]
            return calc_note
    return "COULD NOT GET A VALID NOTE"

##################################
# Main Part of Program
##################################
f = 'piano_a.wav'
freq = get_frequency(f)
note = get_note(freq)
print(freq)
print(note)
