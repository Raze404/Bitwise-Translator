import sys
import binascii
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QComboBox, QStatusBar
)
from PyQt5.QtGui import QClipboard, QFont
from PyQt5.QtCore import Qt

class BitwiseTranslator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bitwise Translator")
        self.setGeometry(150, 150, 600, 400)  # Smaller window size

        self.create_widgets()
        self.create_layout()
        self.clipboard = QApplication.clipboard()

    def create_widgets(self):
        self.title_label = QLabel("Bitwise Translator", self)
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text here...")
        self.text_input.textChanged.connect(self.convert_text_to_binary)

        self.binary_input = QLineEdit(self)
        self.binary_input.setPlaceholderText("Enter binary here...")
        self.binary_input.textChanged.connect(self.convert_binary_to_text)

        self.text_to_binary_label = QLabel("Text to Binary:", self)
        self.binary_to_text_label = QLabel("Binary to Text:", self)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_text_to_binary)

        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_fields)

        self.encoding_combobox = QComboBox(self)
        self.encoding_combobox.addItems(["UTF-8", "ASCII", "Base64", "Hexadecimal", "Octal"])
        self.encoding_combobox.currentIndexChanged.connect(self.update_encoding)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)

        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.text_to_binary_label)
        self.input_layout.addWidget(self.text_input)
        self.input_layout.addWidget(self.binary_to_text_label)
        self.input_layout.addWidget(self.binary_input)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.convert_button)
        self.button_layout.addWidget(self.copy_button)
        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addWidget(self.encoding_combobox)

        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.button_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            background-color: #e6f7ff;
            font-family: Arial, sans-serif;
            font-size: 14px;
        """)
        self.title_label.setStyleSheet("color: #333;")
        self.text_input.setStyleSheet("background-color: #ffffff; padding: 10px;")
        self.binary_input.setStyleSheet("background-color: #ffffff; padding: 10px;")
        self.convert_button.setStyleSheet("background-color: #b3e0ff; padding: 10px;")
        self.copy_button.setStyleSheet("background-color: #b3e0ff; padding: 10px;")
        self.clear_button.setStyleSheet("background-color: #b3e0ff; padding: 10px;")
        self.status_bar.showMessage("Ready")

    def create_layout(self):
        pass

    def convert_text_to_binary(self):
        text = self.text_input.text()
        encoding = self.encoding_combobox.currentText()
        try:
            if encoding == "Base64":
                binary_data = binascii.b2a_base64(text.encode()).decode().strip()
            elif encoding == "Hexadecimal":
                binary_data = binascii.hexlify(text.encode()).decode()
            elif encoding == "Octal":
                binary_data = ' '.join(format(ord(c), '03o') for c in text)
            else:
                binary_data = ' '.join(format(ord(c), '08b') for c in text)
            self.binary_input.setText(binary_data)
            self.status_bar.showMessage("Conversion successful")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.status_bar.showMessage(f"Error: {e}")

    def convert_binary_to_text(self):
        binary_data = self.binary_input.text()
        encoding = self.encoding_combobox.currentText()
        try:
            if encoding == "Base64":
                text = binascii.a2b_base64(binary_data).decode()
            elif encoding == "Hexadecimal":
                text = binascii.unhexlify(binary_data).decode()
            elif encoding == "Octal":
                text = ''.join(chr(int(b, 8)) for b in binary_data.split())
            else:
                text = ''.join(chr(int(b, 2)) for b in binary_data.split())
            self.text_input.setText(text)
            self.status_bar.showMessage("Conversion successful")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.status_bar.showMessage(f"Error: {e}")

    def copy_to_clipboard(self):
        text = self.text_input.text() or self.binary_input.text()
        self.clipboard.setText(text)
        self.status_bar.showMessage("Copied to clipboard")

    def clear_fields(self):
        self.text_input.clear()
        self.binary_input.clear()
        self.status_bar.showMessage("Fields cleared")

    def update_encoding(self):
        self.convert_text_to_binary()
        self.convert_binary_to_text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BitwiseTranslator()
    window.show()
    sys.exit(app.exec_())
