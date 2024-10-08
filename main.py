import sys
from PyQt5.QtWidgets import QApplication
from src.windows.voice_window import VoiceRecognitionApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceRecognitionApp()
    window.show()
    sys.exit(app.exec_())
