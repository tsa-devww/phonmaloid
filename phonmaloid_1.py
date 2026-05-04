import librosa
import numpy as np
from pydub import AudioSegment
from configparser import ConfigParser
config = ConfigParser()
phon_len = 0
samples = []
insyl = []
final = 0
fthd = AudioSegment.empty()

consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'è', 'é']


def process_consonants(i, c, syl):
    if i + 1 < len(syl) and syl[i + 1] == "'":  # soft sign
        print('ь')
    elif c == 'g' and i + 1 < len(syl) and syl[i + 1] == 'n':
        print('gn')
    elif c == 'c' and i + 1 < len(syl) and syl[i + 1] == 'h':
        print('ch')
    elif c == 'r':
        if i + 1 < len(syl) and syl[i + 1] == 'r':
            print('R')
        else:
            if i != 0 and syl[i - 1] == 'r':
                pass
            else:
                print('r')
    if c == 's':
        print('s')
    if c == 'z':
        print('z')
    if c == 't':
        print('t')
    if c == 'd':
        print('d')
    if c == 'n':
        insyl.append(AudioSegment.from_file(r"phonmaloid01/classic_samples/consonanant/c_n_ed.wav"))
    if c == 'm':
        print('m')
    if c == 'l':
        print('l')
    if c == 'p':
        print('p')
    if c == 'b':
        print('b')
    if c == 'f':
        print('f')
    if c == 'v':
        print('v')
    if c == 'k':
        print('k')


def process_vowels(j, i, syl):
    if i == 'a':
        print('a')
    if i == 'e':
        print('e')
    if i == 'i':
        print('i')
    if i == 'o':
        print('o')
    if i == 'u':
        print('u')
    if i == 'y':
        print('y')
    if i == 'è':
        insyl.append(AudioSegment.from_file(r"phonmaloid01\classic_samples\vowel\v_ai_ed.wav"))
    if i == 'é':
        print('é')
    if i == "?":
        print("wain")


# def rhythm_decode():
#     global phon_len
#     for i in rhythm:
#         if i != 1:
#             if float(i) - int(i) == 0.5:
#                 phon_len = int(i) - 0.5 * mspb + mspb/2
#             else:
#                 phon_len = (1/int(i)) * mspb
#         else:
#             phon_len = msfb


def rhythm_decode():
    global phon_len
    if i != 1:
        if float(i) - int(i) == 0.5:
            phon_len = int(i) - 0.5 * mspb + mspb/2
        else:
            phon_len = (1/int(i)) * mspb
    else:
        phon_len = msfb


def lyric_decode():
    global insyl
    for syl in lyrics:
        for j, i in enumerate(syl):
            if i in consonants:
                process_consonants(j, i, syl)
            if i in vowels:
                process_vowels(j, i, syl)
            if i == "-":
                insyl.append(AudioSegment.silent())
        samples.append(insyl)
        insyl = []


AudioSegment.converter = r'<ffmpeg path>'  # this doesn't work but if removed, librosa might break

score = input("score name: ")
config.read(fr'phonmaloid01\scores\{score}', encoding='utf-8')
bpm = config.getint('config', 'bpm')
melody = config.get('config', 'melody').split('/')
rhythm = config.get('config', 'rhythm').split('/')
lyrics = config.get('config', 'lyrics').split('/')
custom_tune = config.getboolean('config', 'custom_tune')
harmony = config.getboolean('config', 'harmony')

mspb = int(60000 / bpm)  # milliseconds per beat
msfb = mspb * 4  # milliseconds per four beats
mstb = mspb * 3  # milliseconds per three beats

song = [melody, rhythm, lyrics]

print(*song, "\n", mspb)
lyric_decode()

for i in samples:
    if samples.index(i) != len(samples):
        for j in i:
            if len(i) == 2:  # CV or CHc only
                fthd = fthd + (j * int(phon_len * 0.1))  # consonant
                fthd = fthd + (j * int(phon_len * 0.9))  # vowel
            elif len(i) == 1: # V only
                fthd = fthd + (j * phon_len)
    final = fthd

print("exporting")
score = final.export("test.wav", format="wav")
