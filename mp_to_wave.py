import os
from pydub import AudioSegment
# from ..audio_data

# path to the mp3 audio data
path = './audio_data/classical_mp3/'

# directory
directory = os.fsencode(path)



# loop through all the data in the directort
for file in os.listdir(directory):
   filename = os.fsdecode(file)
   if filename.endswith(".mp3"): 
      # the mp3 file
      src = f'{path}/{filename}'
      # remove .mp3 and add .wav
      filename = f'{filename[:-4]}.wav'
      # the destination of where we want to save our wav data to
      dst = f'./audio_data/classical_wav/{filename}'
      # create a file where we can save that wav data to
      f = open(dst, 'x') 
      f.close()
      # load the mp3
      sound = AudioSegment.from_mp3(src)
      # convert to wav and save to a directory
      sound.export(dst, format='wav')



def mp3_to_wav(origin:str, destination:str):
   """
   Function to convert all mp3 files from a directory to wav into another
   directory. 
   """
   return