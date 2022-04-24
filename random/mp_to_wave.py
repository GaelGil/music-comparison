import os
from pydub import AudioSegment

path = '../audio_data/mp3_data'

directory = os.fsencode(path)
    
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".mp3"): 
        #  print(os.path.join(directory, filename))
        # print(filename)
        src = f'{path}/{filename}'
        filename = filename[:-4]
        dst = f'../audio_data/wav_data/{filename}.wav'
        print(src)
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format='wav')
