from email.mime import audio
import os
from pydub import AudioSegment
# import sys
# sys.path.append('/path/to/ffmpeg')

# src = './data/Ghost.mp3'
src = './dua_lipa.mp3'

dst = 'dua_lipa.wav'
soud = AudioSegment.from_mp3(src)
soud.export(dst, format='wav')
path = './data'

# directory = os.fsencode(path)
    
# for file in os.listdir(directory):
#      filename = os.fsdecode(file)
#      if filename.endswith(".mp3"): 
#         #  print(os.path.join(directory, filename))
#          src = (f'./new_data/{filename}')
#          dst = f'./new_data/{filename}'
#          print(src)
#          sound = AudioSegment.from_mp3(src)
#          sound.export(dst, format='wav')
