# from utils.preprocessor import Preprocessor
import speech_recognition as sr
from fuzzywuzzy import fuzz

if __name__ == '__main__':
    r = sr.Recognizer()
    with sr.AudioFile("8975-270782-0000 (1).wav") as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
        except:
            print('Sorry.. run again...')
            text=""
    
    text_sample = "us"
    label = "THIRTEENTH LECTURE THE DREAM ARCHAIC REMNANTS AND INFANTILISM IN THE DREAM LET US REVERT TO OUR CONCLUSION THAT THE DREAM WORK UNDER THE INFLUENCE OF THE DREAM CENSORSHIP"
    label = label.lower()
    sr_score = fuzz.ratio(label, text)
    model_score = fuzz.ratio(label, text_sample)

    if sr_score > model_score:
        print("="*30)
        print("Text :", text)
        print("Score :", sr_score)
        print("Sumber :", "SR")
    else:
        print("="*30)
        print("Text :", text_sample)
        print("Score :", model_score)
        print("Sumber :", "Model")
