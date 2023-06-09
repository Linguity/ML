import os
from pydub import AudioSegment
'''
Convert .mp3 audio format to .wav audio format 

'''
folder_path = 'alphabet_dataset'
for folder in os.listdir(folder_path):
    folder1 = os.path.join(folder_path,folder)
    for index, file in enumerate( os.listdir(folder1)):
        input_file = os.path.join(folder_path,folder,file)
        new_path = os.path.join("new_dataset", folder)
        output_file = os.path.join(new_path,"{}_{}.wav".format(folder,index))
        
        # if not os.path.exists(new_path):
        #     os.mkdir(new_path)
        # if os.path.exists(output_file) :
        #     os.remove(output_file)
        sound = AudioSegment.from_mp3(input_file)
        sound.export(output_file, format="wav")