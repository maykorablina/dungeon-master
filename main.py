# main.py

import sys
from PyQt5.QtWidgets import QApplication
from src.windows.voice_window import VoiceRecognitionApp
from src.chat import DungeonMaster

if __name__ == "__main__":
    dm = DungeonMaster('game1')
    app = QApplication(sys.argv)
    window = VoiceRecognitionApp(llm=dm, trigger_word="абоба")
    window.show()
    sys.exit(app.exec_())
