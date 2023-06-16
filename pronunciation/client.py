import requests
import sys
# server url
URL = "http://127.0.0.1:5000/predict"


# audio file we'd like to send for predicting keyword



if __name__ == "__main__":
    path = "data/technology.wav"
    label = "t e c h n o l o g y"
    # open files
    # file = open(FILE_PATH, "rb")

    # package stuff to send and perform POST request
    values = {"file": path, "label": label}
    # r = requests.post(URL, data="data/technology.wav")
    response = requests.post(URL, data = values)


    data = response.json()
    # data = response
    # print(data["hasil"][0])
    print("hasil = " + data["hasil"][0])
    print("label = " + data["label"][0])
    # hasil = data["hasil"]

    # for i in range(len(LABEL)):
    #     print("Predicted keyword: " + hasil[i])
    #     print("label: " + LABEL[i])