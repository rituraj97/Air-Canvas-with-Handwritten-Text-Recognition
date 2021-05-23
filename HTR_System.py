import io
import os
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import pyttsx3


def HTR_System_Method():
    #text to speech
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'--PATH TO THE CREDENTIALS JSON FILE--'

    client = vision.ImageAnnotatorClient()

    FOLDER_PATH = r'--PATH TO THE FOLDER--'
    IMAGE_FILE = r'handwriting.png'

    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content = content)

    response = client.document_text_detection(image = image)

    docText = response.full_text_annotation.text
    print("Text that you entered is : " + docText)
    speak(f"Text that you entered is : {docText}")
    return(docText)