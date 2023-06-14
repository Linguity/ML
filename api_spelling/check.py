def checkresult(transcript, question):
    transcript = transcript.replace(" ", "").lower()
    question = question.lower()
    if transcript != question:
        return print("Wrong")
    return print("Right")

    


