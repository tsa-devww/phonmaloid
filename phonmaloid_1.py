from pydub import AudioSegment
import librosa
import numpy as np

AudioSegment.converter = r"C:\Users\renat\PycharmProjects\phomnaloid\ffmpeg"

melody = []
rhythm = []
lyrics = []

bpm = int(input("bpm? "))

msfb = 60000 / bpm
mspb = msfb / 4

melody = input("melody? ").split("/")
rhythm = input("rhythm? ").split("/")
lyrics = input("lyrics? ").split("/")

song = [melody, rhythm, lyrics]

print(*song, "\n", msfb)
