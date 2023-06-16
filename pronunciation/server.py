import os
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import sys
import requests
import speech_recognition as sr
from fuzzywuzzy import fuzz

# inisiasi flask app
app = Flask(__name__)
#LOAD MODEL
model = tf.saved_model.load(
'asr-30epoch-full_model', tags=None, options=None
)

r = sr.Recognizer()


@app.route("/predict", methods=["POST"])
def predict():
    # FILE_PATH = ["data/performance.wav", "data/technology.wav"]
    # LABEL = ["p e r f o r m a n c e", "t e c h n o l o g y"]
    path_audio = "audio.wav"
    wavs = [request.form.get("file")]
    label = [request.form.get("label")]
    url = wavs[0]

    #D O W N L O A D
    response = requests.get(url)
    open(path_audio, "wb").write(response.content)

    #ENCODING SESUAI MAPPING & CREATING DATASET
    data = tf.data.Dataset.from_tensor_slices(
    ([path_audio], label)
    )
    data = (
        data.map(encode_single_sample, num_parallel_calls=tf.data.AUTOTUNE)
        .padded_batch(32)
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    # Proses inference
    # predictions = ""
    for batch in data:
        X, y = batch
        batch_predictions = model.signatures['serving_default'](input=X)
        for keys, value in batch_predictions.items():
        # print(value)
            decoded_pred = decode_batch_predictions(value)
            predictions = decoded_pred


    with sr.AudioFile(path_audio) as source:
        audio_text = r.listen(source)
        try:
            text_sr = r.recognize_google(audio_text)
        except:
            text_sr = ""
    
    sr_score = fuzz.ratio(label, text_sr)
    model_score = fuzz.ratio(label, predictions)

    if sr_score > model_score:
        final_score = sr_score
        final_text = text_sr
        sumber = "sr"
    else:
        final_score = model_score
        final_text = predictions
        sumber = "model"

    if final_text == label:
        output = True
    else:
        output = False
    
    return jsonify ({"hasil": final_text, "label": label, "score": final_score, "sumber": sumber, "check": output})

#Pengolahan Audio
def encode_single_sample(wav_file, label):
    #MAPPING untuk membuat vocabulary tokenizer
    characters = [x for x in "abcdefghijklmnopqrstuvwxyz'?! "]
    # Mapping untuk karakter (abcd) menjadi angka (1234)
    char_to_num = keras.layers.StringLookup(vocabulary=characters, oov_token="")
    # 1. Membuka file wav
    file = tf.io.read_file(wav_file)
    # 2. Proses decode file
    audio, _ = tf.audio.decode_wav(file)
    audio = tf.squeeze(audio, axis=-1)
    # 3. Ubah tipe data menjadi float
    audio = tf.cast(audio, tf.float32)
    # 4. Proses pembuatan spectogram
    spectrogram = tf.signal.stft(
        audio, frame_length=256, frame_step=160, fft_length=384
    )

    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)
    # 5. Normalisasi
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)
    #Pengolahan label
    # 6. Case folding
    label = tf.strings.lower(label)
    # 7. Split split menjadi perhuruf
    label = tf.strings.unicode_split(label, input_encoding="UTF-8")
    # 8. Merubah karakter/huruf menjadi angka sesuai mapping (tokenizing)
    label = char_to_num(label)

    return spectrogram, label


# Pengolahan hasil prediksi menjadi kalimat
def decode_batch_predictions(pred):
    #MAPPING untuk membuat vocabulary tokenizer
    characters = [x for x in "abcdefghijklmnopqrstuvwxyz'?! "]
    # Mapping untuk karakter (abcd) menjadi angka (1234)
    char_to_num = keras.layers.StringLookup(vocabulary=characters, oov_token="")
    # Membuat mapping sebaliknya (angka menjadi karakter)
    num_to_char = keras.layers.StringLookup(
        vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
    )
    # Membuat array berisi angka 1 sesuai ukuran hasil prediksi
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Pengolahan hasil prediksi menggunakan ctc dengan greedy search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0]
    # Proses perangkaian dan perubahan kata 
    output_text = []
    for result in results:
        result = tf.strings.reduce_join(num_to_char(result)).numpy().decode("utf-8")
        output_text.append(result)
    return output_text

if __name__ == "__main__":
    app.run(debug=False)