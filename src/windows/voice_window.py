import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QEventLoop

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VoiceRecognitionApp(QWidget):
    def __init__(self, llm, trigger_word="арбуз"):
        super().__init__()

        self.setWindowTitle("Voice Recognition with Trigger Word")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QVBoxLayout()

        self.text_label = QLabel("Listening for the trigger word...")
        self.layout.addWidget(self.text_label, alignment=Qt.AlignCenter)

        # self.restart_button = QPushButton("Start Over")
        # self.restart_button.clicked.connect(self.restart_process)
        # self.layout.addWidget(self.restart_button, alignment=Qt.AlignCenter)
        # self.restart_button.hide()

        self.setLayout(self.layout)

        self.recognizer = sr.Recognizer()
        self.llm = llm
        self.trigger_word = trigger_word
        self.is_trigger_word_detected = False

        self.listen_thread = ListenThread(self.recognizer)
        self.listen_thread.recognized_text.connect(self.process_recognized_text)

        self.speak_thread = None  # Поток речи инициализируется как None
        self.listen_thread.start()  # Запускаем прослушивание

        logging.info("Application started and listening for the trigger word.")

    def process_recognized_text(self, text):
        logging.info(f"Recognized text: {text}")
        self.text_label.setText(f"Recognized Text: {text}")

        if self.trigger_word in text.lower():
            self.is_trigger_word_detected = True
            self.text_label.setText(f"Trigger word '{self.trigger_word}' detected! Awaiting further input...")
            logging.info(f"Trigger word '{self.trigger_word}' detected.")
        elif self.is_trigger_word_detected:
            self.generate_response(text)
            self.is_trigger_word_detected = False

    def generate_response(self, text):
        logging.info("Stopping listening and generating response.")
        self.listen_thread.stop_listening()

        response = self.llm.chat(text)
        self.text_label.setText(f"AI Response: {response}")
        logging.info(f"Generated AI response: {response}")

        self.speak_thread = SpeakThread(response)
        self.speak_thread.finished.connect(self.on_speech_finished)
        self.speak_thread.start()

    def on_speech_finished(self):
        logging.info("Speech finished.")
        self.restart_process()
        # self.restart_button.show()

    def restart_process(self):
        logging.info("Restarting process.")
        self.text_label.setText("Listening for the trigger word...")
        self.listen_thread.restart_listening()
        # self.restart_button.hide()

    def closeEvent(self, event):
        event.ignore()

class SpeakThread(QThread):
    finished = pyqtSignal()
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.engine = pyttsx3.init()

        self.engine.connect('finished-utterance', self.on_finish_utterance)

    def run(self):
        logging.info(f"Starting speech synthesis for: {self.text}")
        self.engine.say(self.text)
        self.engine.runAndWait()

    def on_finish_utterance(self, name, completed):
        logging.info(f"Speech synthesis finished for {name}, completed: {completed}")
        self.finished.emit()

class ListenThread(QThread):
    recognized_text = pyqtSignal(str)

    def __init__(self, recognizer, parent=None):
        super().__init__(parent)
        self.recognizer = recognizer
        self.running = True

    def run(self):
        logging.info("Listening thread started.")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

            while self.running:
                try:
                    logging.info("Listening for speech input.")
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
                    recognized_text = self.recognizer.recognize_google(audio, language="ru-RU")
                    self.recognized_text.emit(recognized_text)
                except sr.UnknownValueError:
                    logging.warning("Speech not recognized, trying again.")
                    continue
                except sr.RequestError as e:
                    logging.error(f"Could not request results; {e}")
                    continue

    def restart_listening(self):
        if not self.isRunning():
            logging.info("Restarting listening thread.")
            self.running = True
            self.start()

    def stop_listening(self):
        if self.isRunning():
            logging.info("Stopping listening thread.")
            self.running = False
            self.quit()
            self.wait()
