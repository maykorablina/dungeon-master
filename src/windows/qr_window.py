# src/windows/qr_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class QRWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Window")
        self.setGeometry(300, 300, 400, 400)

        layout = QVBoxLayout()

        self.setLayout(layout)
