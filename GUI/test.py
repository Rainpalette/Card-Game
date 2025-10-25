import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Card Game")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon("Afallen.jpg"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # ---------------- 左边标题布局 ----------------
        self.vbox_left = QVBoxLayout()
        self.text_label = QLabel("Card Game")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 60px; font-weight: bold;")
        self.vbox_left.addStretch(1)  # 上方弹性空间
        self.vbox_left.addWidget(self.text_label)
        self.vbox_left.addStretch(1)  # 下方弹性空间

        # ---------------- 右边按钮布局 ----------------
        self.button_layout = QVBoxLayout()
        self.create_deck_button = QPushButton("Deck")
        self.compendium_button = QPushButton("Compendium")
        self.game_start_button = QPushButton("Game Start")

        self.button_layout.addStretch(1)  # 上方弹性空间
        self.button_layout.addWidget(self.create_deck_button)
        self.button_layout.addWidget(self.compendium_button)
        self.button_layout.addWidget(self.game_start_button)
        self.button_layout.addStretch(1)  # 下方弹性空间

        # ---------------- 主布局 ----------------
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.vbox_left)     # 左边标题
        self.main_layout.addLayout(self.button_layout) # 右边按钮

        # 设置横向比例 2:1
        self.main_layout.setStretch(0, 2)  # 左边 2/3
        self.main_layout.setStretch(1, 1)  # 右边 1/3

        self.central_widget.setLayout(self.main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
