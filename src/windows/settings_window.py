# src/windows/settings_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QPushButton
from PyQt5.QtCore import Qt


class SettingsWindow(QWidget):
    def __init__(self, voice_engine):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 300)
        self.voice_engine = voice_engine

        layout = QVBoxLayout()

        self.speed_label = QLabel("Speech Rate:")
        layout.addWidget(self.speed_label)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(300)
        self.speed_slider.setValue(150)
        layout.addWidget(self.speed_slider)

        # Volume setting
        self.volume_label = QLabel("Volume:")
        layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        layout.addWidget(self.volume_slider)

        # Voice selection
        self.voice_label = QLabel("Voice:")
        layout.addWidget(self.voice_label)

        self.voice_combo = QComboBox()
        self.voices = self.voice_engine.getProperty('voices')
        for voice in self.voices:
            self.voice_combo.addItem(voice.name)
        layout.addWidget(self.voice_combo)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def apply_settings(self):
        rate = self.speed_slider.value()
        self.voice_engine.setProperty('rate', rate)

        volume = self.volume_slider.value() / 100
        self.voice_engine.setProperty('volume', volume)

        selected_voice = self.voices[self.voice_combo.currentIndex()].id
        self.voice_engine.setProperty('voice', selected_voice)

        self.close()
