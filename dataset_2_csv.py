from csv import writer
import os
i=1
with open('dataset.csv','a') as csv:
    writer_object = writer(csv)
    writer_object.writerow(['no','wavpath','transcript'])
    
    folder_path = 'new_dataset'
    for folder in os.listdir(folder_path):
        folder1 = os.path.join(folder_path,folder)
        for index, file in enumerate( os.listdir(folder1)):
            wavpath = os.path.join(folder1,file)
        
            writer_object.writerow([i, wavpath, folder])
            i+=1
csv.close()