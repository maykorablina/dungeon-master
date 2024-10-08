# src/windows/voice_window.py

import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class VoiceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dungeon mASSter")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QVBoxLayout()

        self.button = QPushButton("Start Recording")
        self.button.clicked.connect(self.start_recording)
        self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.text_label = QLabel('')
        self.layout.addWidget(self.text_label, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def start_recording(self):
        self.text_label.setText("Recording...")
        self.record_audio()

    def record_audio(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.text_label.setText("Listening...")

            try:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=None)
                self.text_label.setText("Processing...")

                text = self.recognizer.recognize_google(audio, language="ru-RU")
                self.text_label.setText(f"Recognized Text: {text}")

                self.speak_text(text)

            except sr.UnknownValueError:
                self.text_label.setText("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                self.text_label.setText(f"Could not request results; {e}")

    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
