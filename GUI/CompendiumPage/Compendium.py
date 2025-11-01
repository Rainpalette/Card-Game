from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel,QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))
from GUI.DeckCreationPage.CreateDeckPage import *
from GUI.BattlePage.show_card_page import Card

class CardInCompendium(Card):
    def __init__(self, name="", image_path=""):
        super().__init__(name, image_path)

class CompendiumPage(QWidget):
    send_name = pyqtSignal(str)
    leftClicked = pyqtSignal(int)
    switch_to_page = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        # Create main layout as grid
        self.main_layout = QGridLayout(self)
        # Create a container widget for the card grid
        self.card_container = QWidget()
        self.page_layout = QGridLayout(self.card_container)
        # self.setFixedSize(200,250)
        self.page = 1
        self.max_page = 10
        self.card_list = []
        # Set up navigation buttons
        self.next_button = QPushButton(">")  # Changed to arrow symbol
        self.next_button.setFixedSize(40, 80)  # Made taller for better visibility
        self.next_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                background-color: #f0f0f0;
                border-radius: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.next_button.clicked.connect(self.next_page)
        self.next_button.hide()

        self.back_button = QPushButton("<")  # Changed to arrow symbol
        self.back_button.setFixedSize(40, 80)  # Made taller for better visibility
        self.back_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                background-color: #f0f0f0;
                border-radius: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.back_button.clicked.connect(self.previous_page)
        self.back_button.hide()

        self.exit_button= QPushButton("Back")
        self.exit_button.setFixedSize(50,50)
        self.exit_button.setStyleSheet("font-size: 20px;")
        self.exit_button.clicked.connect(self.on_click_exit_deck)

        with open(r"Data\Card.json", "r", encoding="utf-8") as f:
            self.cards_info = json.load(f)

        self.card_info_list = []
        for card in self.cards_info["cards"]:
            card_info = {
                "name": card["name"],
                "description": card["description"],
                "mana_cost": card["mana_cost"],
                "cooldown": card["cooldown"],
                "type": card["type"],
                "rarity": card["rarity"],
                "image_path": card["image_path"],
                "backstory": card["backstory"]
            }
            self.card_info_list.append(card_info)

        card_count = 0
        for row in range(1,3):
            for col in range(4):
                if card_count<8:
                    card = CardInDeck(self.cards_info['cards'][card_count]['name'], self.cards_info['cards'][card_count]['image_path'])
                    card.id = card_count+1
                    card.card_image.setScaledContents(True)
                    card.leftClicked.connect(self.on_card_left_clicked)
                    #card.rightClicked.connect(self.on_card_right_clicked)
                    # card.clicked.connect(self.on_card_left_clicked)
                    self.card_list.append(card)
                    self.page_layout.addWidget(card, row+2, col+1)
                    card_count +=1
        self.next_button.show()
        
        # Add exit button to top-left corner
        self.main_layout.addWidget(self.exit_button, 0, 0, Qt.AlignTop | Qt.AlignLeft)

        # Add navigation buttons to middle left and right
        self.main_layout.addWidget(self.back_button, 1, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.main_layout.addWidget(self.next_button, 1, 2, Qt.AlignVCenter | Qt.AlignRight)

        # Add card container to center
        self.main_layout.addWidget(self.card_container, 1, 1)
        
        # Add stretches to create margins and center the content
        self.main_layout.setColumnStretch(0, 1)  # Left margin
        self.main_layout.setColumnStretch(1, 10)  # Center column
        self.main_layout.setColumnStretch(2, 1)  # Right margin
        self.main_layout.setRowStretch(0, 1)  # Top margin
        self.main_layout.setRowStretch(1, 10)  # Center row
        self.main_layout.setRowStretch(2, 1)  # Bottom margin
    
    def switch_page(self):
        current_index = (self.page-1)*8
        
        if self.page>1:
            self.back_button.show()
        else:
            self.back_button.hide()
        if self.max_page>self.page:
            self.next_button.show()
        else:
            self.next_button.hide()
           
        card_count = 0
        for i in range(8):
            if current_index+card_count < len(self.cards_info['cards']):
                self.card_list[card_count].name = self.cards_info['cards'][current_index+card_count]['name']
                self.card_list[card_count].image_path = self.cards_info['cards'][current_index+card_count]['image_path']
                self.card_list[card_count].leftClicked.connect(self.on_card_left_clicked)
                # self.card_list[card_count].rightClicked.connect(self.on_card_right_clicked)
                self.card_list[card_count].refresh_card()
            else:
                # self.card_list[card_count].name = ""
                # self.card_list[card_count].image_path = ""
                # self.card_list[card_count].refresh_card()
                self.card_list[card_count].clear_card()
            card_count+=1
            # self.card_list[card_count].name = self.cards_info['cards'][current_index+card_count]['name']
            # self.card_list[card_count].image_path = "GUI/BattlePage/Afallen.jpg"
            # self.card_list[card_count].refresh_card()
            # card_count+=1

    # def on_card_right_clicked(self, name):
    #     pass

    def on_card_left_clicked(self, name):
        self.send_name.emit(name)
    
    def next_page(self):
        self.page+=1
        self.switch_page()
        print(self.page)

    def previous_page(self):
        self.page-=1
        self.switch_page()
        print(self.page)
    
    def on_click_exit_deck(self):
        self.switch_to_page.emit(0)
