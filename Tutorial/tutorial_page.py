from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))

class TutorialPage(QWidget):
    switch_to_page = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.page_layout = QGridLayout(self)

        self.title_label = QLabel("Tutorial")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color:white;")
        self.page_layout.addWidget(self.title_label, 0, 1, alignment=Qt.AlignCenter)

        self.tutorial_text = QLabel(
            "Welcome to the Card Game!\n\n"
            "In this game, you will build a deck of cards and battle against various mobs.\n\n"
            "Each card has unique effects that can help you defeat your opponents.\n\n"
            "Use strategy and skill to outsmart your enemies and emerge victorious!\n\n"
            "Good luck and have fun!"
        )
        self.tutorial_text.setStyleSheet("font-size: 18px; color:white;")
        self.tutorial_text.setWordWrap(True)
        self.page_layout.addWidget(self.tutorial_text, 1, 0, 1, 3)

        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet("font-size: 20px;")
        self.back_button.clicked.connect(self.on_click_back)
        self.page_layout.addWidget(self.back_button, 2, 1, alignment=Qt.AlignCenter)

    def on_click_back(self):
        self.switch_to_page.emit(0)  # Assuming 0 is the index for the main page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tutorial_page = TutorialPage()
    tutorial_page.show()
    sys.exit(app.exec_())