from pydub import AudioSegment

filename="own/data/mr.wav"

print(AudioSegment.from_file(filename, format="wav").frame_rate)