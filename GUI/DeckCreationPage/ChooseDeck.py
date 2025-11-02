from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QGridLayout, QVBoxLayout, QLabel,QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import sys
import os
import json


class DeckButton(QPushButton):
    deck_clicked = pyqtSignal(int)  # Custom signal for deck selection
    
    def __init__(self):
        super().__init__()
        self.deck_id = 0
        self.name = f"Deck {self.deck_id}"
        self.setMinimumSize(250, 170)
        # self.setStyleSheet("font-size: 20px;")
        self.setStyleSheet("""
            QPushButton {
                font-size: 35px;
                border-image: url(buttonimage.jpg) 0 0 0 0 stretch stretch;
                color: white;
                border: none;
            }
            QPushButton:hover {
                border-image: url(buttonimage.jpg) 0 0 0 0 stretch stretch;
                background-color: rgba(255, 255, 255, 30);
                color:#536d82
            }
        """)
        self.setText(self.name)

    def change_text(self, new_text):
        self.setText(new_text)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.deck_clicked.emit(self.deck_id)  # Emit our custom signal

class ChooseDeckPage(QWidget):
    switch_to_page = pyqtSignal(int)
    search_deck = pyqtSignal(int)
    def __init__(self, deck_stage):
        super().__init__()
        self.deck = deck_stage
        self.page_layout = QGridLayout(self)
        self.exit_button= QPushButton("Back")
        self.exit_button.setFixedSize(50,50)
        self.exit_button.setStyleSheet("font-size: 20px;")
        self.exit_button.clicked.connect(self.on_click_exit_deck)

        self.set_current_deck_label = QLabel(f"Current Deck:\n{self.deck.in_use_deck_name}")
        self.set_current_deck_label.setStyleSheet("font-size: 18px; font-weight: bold;color:white;")
        self.page_layout.addWidget(self.set_current_deck_label, 0, 3)

        # self.set_current_deck_button.setFixedSize(150,50)
        # self.set_current_deck_button.setStyleSheet("font-size: 20px;")
        # self.set_current_deck_button.clicked.connect(self.on_click_set_current_deck)
        
        self.page_layout.addWidget(self.exit_button,0,0) 
        # self.page_layout.addWidget(self.set_current_deck_button, 0, 3)
        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(30)
        for row in range(3):
            for col in range(3):
                card = DeckButton()
                card.deck_id = row*3+col
                print(f"Creating button for deck ID: {card.deck_id}")
                self.button_layout.addWidget(card, row+1, col+1)
                card.deck_clicked.connect(self.on_click_create_deck)  
        self.page_layout.addLayout(self.button_layout, 2, 2)

        self.page_layout.setColumnStretch(0, 1)
        self.page_layout.setColumnStretch(1, 1)
        self.page_layout.setColumnStretch(3, 1)
        self.page_layout.setRowStretch(0, 1)
        self.page_layout.setRowStretch(1, 1)
        self.page_layout.setRowStretch(3, 1)
        
        # Add margins around the layout
        self.page_layout.setContentsMargins(20, 20, 20, 20)

    def on_click_exit_deck(self):
        self.switch_to_page.emit(0)

    def on_click_create_deck(self, deck_id):
        print(f"Deck clicked: {deck_id}") 
        self.search_deck.emit(deck_id)
    
    def change_button_text(self, deck_id, new_text):
        button = self.button_layout.itemAtPosition(deck_id//3 + 1, deck_id%3 + 1).widget()
        if button:
            button.change_text(new_text)

    def refresh_current_deck_label(self):
        print("Refreshing current deck label")
        print(f"Current deck name: {self.deck.current_deck_name}")
        self.set_current_deck_label.setText(f"Current Deck:\n{self.deck.current_deck_name}")
    # def on_click_set_current_deck(self):
    #     print("Set Current Deck button clicked")
    #     self.search_deck.emit(-1)  # Emit signal to set current deck


class CardDeckInformation(QWidget):
    switch_to_page = pyqtSignal(int)
    send_deck_name = pyqtSignal(str)
    def __init__(self, create_deck_page):
        super().__init__()
        self.create_deck_page = create_deck_page
        
        # Main layout
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(20, 20, 20, 20)
        
        # Back button in top-left corner
        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(50, 50)
        self.back_button.clicked.connect(self.on_click_back)
        self.back_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                border-radius: 25px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.page_layout.addWidget(self.back_button, 0, 0, Qt.AlignTop | Qt.AlignLeft)

        # Center container for deck name input and submit button
        self.center_container = QWidget()
        self.setting_layout = QVBoxLayout(self.center_container)
        self.setting_layout.setSpacing(20)  # Increase spacing between elements
        
        # Deck name input layout
        self.name_layout = QHBoxLayout()
        self.deck_name_label = QLabel("Deck Name:")
        self.deck_name_label.setStyleSheet("font-size: 18px; font-weight: bold;color:white;")
        self.name_layout.addWidget(self.deck_name_label)
        
        self.deck_name = QLineEdit()
        self.deck_name.setMinimumWidth(300)  # Make input field wider
        self.deck_name.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 10px;
                background-color: white;

            }
            QLineEdit:focus {
                border-color: #a0a0a0;
            }
        """)
        self.name_layout.addWidget(self.deck_name)
        
        # Add layouts to center container
        self.setting_layout.addStretch(1)  # Add space at top
        self.setting_layout.addLayout(self.name_layout)
        
        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(200, 50)  # Make button wider
        #make a button with background color black
        self.submit_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: black;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            
        """)
        
        # QPushButton:hover {
        #         background-color: #45a049;
            # }
        self.submit_button.clicked.connect(self.on_click_submit)
        self.setting_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)
        self.setting_layout.addStretch(1)  # Add space at bottom
        
        # Add center container to main layout
        self.page_layout.addWidget(self.center_container, 1, 1)
        
        # Add stretches for margins and centering
        self.page_layout.setColumnStretch(0, 1)
        self.page_layout.setColumnStretch(1, 8)
        self.page_layout.setColumnStretch(2, 1)
        self.page_layout.setRowStretch(0, 1)
        self.page_layout.setRowStretch(1, 8)
        self.page_layout.setRowStretch(2, 1)
    
    def on_click_back(self):
        self.switch_to_page.emit(8)

    def on_click_submit(self):
        self.create_deck_page.current_deck_name = self.deck_name.text()
        self.switch_to_page.emit(5)
        self.send_deck_name.emit(self.deck_name.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardDeckInformation()
    window.show()
    sys.exit(app.exec_())