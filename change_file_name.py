import os

def change_name(root_path):
    split_path = os.path.join(root_path,"TEST")
    for folders in os.listdir(split_path):
        folders_path = os.path.join(split_path,folders)
        for index, files in enumerate(os.listdir(folders_path)):
                old_name = os.path.join(folders_path,files)
                new_name = os.path.join(folders_path,"TEST_{}_{}.wav".format(folders,index))
                os.rename(old_name,new_name)
                # print(old_name)
                # if os.path.exists(new_name):
                #     os.remove(new_name)
if __name__ == "__main__":
    change_name("dataset")