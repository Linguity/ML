from flask import Flask,request, jsonify
import speech_recognition as sr
import urllib.request as ur

app = Flask(__name__)

@app.route("/spelling", methods = ["POST"])

def predict():
    file_path = 'audio/spelling.wav'
    audio_file = request.args.get('file')
    label = request.args.get('label')
    ur.urlretrieve (audio_file, file_path)   
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
        try:
            transcript = r.recognize_vosk(audio)[14:-3]
            
        except sr.UnknownValueError:
            unknown = "Could not understand audio"
        except sr.RequestError as e:
            requesterror = "Request error; {0}".format(e)
            
    return jsonify(transcripts = audio_file, labels = label, prediction = transcript, checkk = checkresult(transcript,label))

def checkresult(prediction_results, question):
    prediction_results = prediction_results.replace(" ", "").lower()
    question = question.lower()
    if prediction_results != question:
        return  False
    return True
if __name__ == '__main__':
    app.run(host = 'localhost', port = 9000)