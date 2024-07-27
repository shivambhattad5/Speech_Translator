from flask import Flask, render_template, request
import googletrans
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)

languages = googletrans.LANGUAGES

def get_language_code(language_name):
    for code, name in languages.items():
        if name.lower() == language_name.lower():
            return code
    return None

@app.route('/')
def index():
    return render_template('index.html', languages=languages)

@app.route('/translate', methods=['POST'])
def translate():
    input_language_name = request.form['input_language']
    output_language_name = request.form['output_language']

    input_language_code = get_language_code(input_language_name)
    output_language_code = get_language_code(output_language_name)

    if not input_language_code or not output_language_code:
        return render_template('index.html', languages=languages, error="Invalid language name entered.")

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now")
        voice = recognizer.listen(source)
        text = recognizer.recognize_google(voice, language=input_language_code)

    translator = googletrans.Translator()
    translation = translator.translate(text, dest=output_language_code)

    tts = gTTS(text=translation.text, lang=output_language_code)
    tts.save("static/hello.mp3")
    return render_template('index.html', languages=languages, translated_text=translation.text)

if __name__ == '__main__':
    app.run(debug=True)
