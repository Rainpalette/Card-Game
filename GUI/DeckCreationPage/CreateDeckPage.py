from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel,QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))
from Card.DeckStage import *
from GUI.BattlePage.show_card_page import Card, CardDetailPage


ds = DeckStage()
class CardInDeck(Card):
    leftClicked = pyqtSignal(str)
    def __init__(self, name="", image_path=""):
        super().__init__(name, image_path)
        self.setFixedSize(180, 225)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftClicked.emit(self.name)
        elif event.button() == Qt.RightButton:
            self.rightClicked.emit(self.name)

class CardShowcase(Card):
    leftClicked = pyqtSignal(str)
    rightClicked = pyqtSignal(str)
    def __init__(self, name="", image_path=""):
        super().__init__(name, image_path)
        self.name = name
        self.image_path = image_path
        self.setFixedSize(140, 175)
        self.card.setStyleSheet("background-color: #C19A6B;")
        self.card.setStyleSheet("""
            QWidget{
                border-radius: 8px;
                border: 2px solid #8b5a2b;
                font-size:13px;
                                }""")
        self.setStyleSheet("""
            QWidget {
                background-color: #caa472;
                
            }
            QWidget:hover {
                background-color: #d4b483;
                
            }
        """)
        if self.name=="":
            self.setStyleSheet("background-color: #C19A6B;")
            self.card.setStyleSheet("background-color: #C19A6B;")
            self.card_image.clear()
            # self.disconnect()
        # self.setStyleSheet("font-size:13px;")
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftClicked.emit(self.name)
        elif event.button() == Qt.RightButton:
            self.rightClicked.emit(self.name)

    def refresh_card(self):
        self.card_name.setText(self.name)
        self.pixmap = QPixmap(self.image_path).scaled(150,350,Qt.KeepAspectRatio)
        self.card_image.setPixmap(self.pixmap)
        if not self.name=="":
            self.card.setStyleSheet("background-color: #C19A6B;")
            self.card.setStyleSheet("""
                QWidget{
                    border-radius: 8px;
                    border: 2px solid #8b5a2b;
                    font-size:13px;
                                    }""")
            self.setStyleSheet("""
                QWidget {
                    background-color: #caa472;
                    
                }
                QWidget:hover {
                    background-color: #d4b483;
                    
                }
            """)
        else:
            self.setStyleSheet("background-color: #C19A6B;")
            self.card.setStyleSheet("background-color: #C19A6B;")
            self.card_image.clear()
            self.card_name.setText("")
            # self.disconnect()
    
    def set_card_name(self,name):
        self.name =name

class CardShowcaseList(QWidget):
    def __init__(self):
        super().__init__()
        self.page_layout = QGridLayout(self)
        with open(r"Data\Card.json", "r", encoding="utf-8") as f:
            self.cards_info = json.load(f)

        self.card_info_list = []
        for card in self.cards_info["cards"]:
            card_info = {
                "name": card["name"],
                "description": card["description"],
                "mana_cost": card["mana_cost"],
                "cooldown": card["cooldown"]
            }
            self.card_info_list.append(card_info)
        for card_row in range(8):
            card_showcase = CardShowcase(self.card_info_list[card_row]["name"], "GUI/BattlePage/Afallen.jpg")
            #card_showcase.leftClicked.connect(self.on_card_left_clicked)
            self.page_layout.addWidget(card_showcase, 1, card_row+1)

class CreateDeckPage(QWidget):
    switch_to_page = pyqtSignal(int)
    change_to_page = pyqtSignal(int)
    send_name = pyqtSignal(str)
    send_card_name = pyqtSignal(str)
    send_showcase_card_name = pyqtSignal(str)
    save_deck = pyqtSignal(dict)
    set_current_deck = pyqtSignal(str)
    error_message = pyqtSignal(str)
    switch_to_returnable_page = pyqtSignal(int)
    def __init__(self,deck=DeckStage()):
        super().__init__()
        self.deck = deck
        self.deck_name = ""
        self.card = Card()
        self.card = CardDetailPage()
        self.page_layout = QGridLayout()
        self.deck_page_layout = QGridLayout(self)
        self.current_deck_name = ""
        self.page = 1
        self.max_page = 2
        self.card_list = []
        self.card_showcase_data_list = []  # Will hold the data for displayed cards
        self.card_showcase_list = []  # Will hold the actual card widgets

        

        self.next_button = QPushButton("next")
        self.next_button.setFixedSize(50,50)
        self.next_button.setStyleSheet("font-size: 20px;")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.hide()

        self.back_button = QPushButton("back")
        self.back_button.setFixedSize(50,50)
        self.back_button.setStyleSheet("font-size: 20px;")
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
                "cooldown": card["cooldown"]
            }
            self.card_info_list.append(card_info)
        self.card_showcase_layout = QGridLayout()
        # self.card_showcase_layout.addWidget(self.exit_button,0,0)
        count = 0
        for card_row in range(8):
            # card_showcase = CardShowcase(self.card_info_list[card_row]["name"], "GUI/BattlePage/Afallen.jpg")
            if count <= len(self.card_showcase_data_list)-1:
                card_showcase = CardShowcase(self.card_showcase_data_list[count]["name"], "GUI/BattlePage/Afallen.jpg")
                card_showcase.leftClicked.connect(self.on_card_right_clicked)
                card_showcase.rightClicked.connect(self.delete_card_showcase)
                self.card_showcase_layout.addWidget(card_showcase, 1, card_row)
                self.card_showcase_list.append(card_showcase)
                count+=1
            else:
                card_showcase = CardShowcase()
                self.card_showcase_layout.addWidget(card_showcase, 1, card_row)
                self.card_showcase_list.append(card_showcase)

                # if not card_showcase.name=="":
                #     card_showcase.leftClicked.connect(self.on_card__right_clicked)
        
        card_count = 0
        for row in range(1,3):
            for col in range(4):
                if card_count<8:
                    card = CardInDeck(self.cards_info['cards'][card_count]['name'], "GUI/BattlePage/Afallen.jpg")
                    card.id = card_count+1
                    card.leftClicked.connect(self.on_card_left_clicked)
                    card.rightClicked.connect(self.on_card_right_clicked)
                    # card.clicked.connect(self.on_card_left_clicked)
                    self.card_list.append(card)
                    self.page_layout.addWidget(card, row+2, col+1)
                    card_count +=1
        self.next_button.show()
        self.page_layout.addWidget(self.next_button,3,5)
        self.page_layout.addWidget(self.back_button, 3,0)
        
        # self.page_layout.setRowStretch(1,1)
        # self.page_layout.setRowStretch(4,1)
        self.deck_page_layout.addWidget(self.exit_button,0,0)
        self.deck_page_layout.addLayout(self.card_showcase_layout,1,1)
        self.deck_page_layout.addLayout(self.page_layout,2,1)

        self.deck_name_label = QLabel("Deck Name")
        self.deck_name_label.setStyleSheet("font-size: 20px;")
        self.deck_page_layout.addWidget(self.deck_name_label,0,1)

        self.deck_save_button = QPushButton("Save")
        self.deck_save_button.setFixedSize(50,50)
        button_layout = QVBoxLayout()
        self.set_current_deck_button = QPushButton("Set\nCurrent\nDeck")
        self.set_current_deck_button.setFixedSize(50,60)
        self.set_current_deck_button.setStyleSheet("font-size: 12px;")
        self.set_current_deck_button.clicked.connect(self.set_as_current_deck)

        button_layout.addWidget(self.deck_save_button)
        button_layout.addWidget(self.set_current_deck_button)
        self.deck_page_layout.addLayout(button_layout,0,2)
        self.deck_save_button.setStyleSheet("font-size: 20px;")
        self.deck_save_button.clicked.connect(self.save_card_deck)

        self.deck_page_layout.setColumnStretch(0,1)
        self.deck_page_layout.setColumnStretch(1,1)
        self.deck_page_layout.setColumnStretch(2,5)
        self.setLayout(self.deck_page_layout)

        #self.page_layout.setColumnStretch(0,1)
        #self.page_layout.setColumnStretch(4,1)

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
            self.card_list[card_count].name = self.cards_info['cards'][current_index+card_count]['name']
            self.card_list[card_count].image_path = "GUI/BattlePage/Afallen.jpg"
            self.card_list[card_count].refresh_card()
            card_count+=1

    def next_page(self):
        self.page+=1
        self.switch_page()
        print(self.page)

    def previous_page(self):
        self.page-=1
        self.switch_page()
        print(self.page)
                    
    def on_card_left_clicked(self,name):
        self.switch_to_page.emit(6)
        self.send_card_name.emit(name)
    
    def on_click_exit_deck(self):
        self.switch_to_page.emit(8)
        self.current_deck_name = ""
    
    def on_card_right_clicked(self,name):
        # self.change_to_page.emit(4)
        self.send_name.emit(name)
    
    def on_click_save_deck(self):
        card_deck = []
        for card_showcase_data in self.card_showcase_data_list:
            card_deck.append(card_showcase_data)

    def delete_card_showcase(self,name):
        self.send_showcase_card_name.emit(name)
        # Find and clear the card data
        for card_data in self.card_showcase_data_list:
            if card_data["name"] == name:
                card_data["name"] = ""
                card_data["image_path"] = ""
                break
        self.refresh_page()

    def delete_card(self,name):
        delete_card = True
        for card in self.card_showcase_list:
            if delete_card and card.name == name:
                print("delete gate")
                card.set_card_name("")
                card.image_path = ""
                try:
                    card.leftClicked.disconnect()
                    card.rightClicked.disconnect()
                except TypeError:
                    pass  # Already disconnected
                card.refresh_card()
                delete_card = False
                break
    
    def refresh_deck_name(self, new_name):
        self.deck_name_label.setText(new_name)
        self.deck_name = new_name

    def set_as_current_deck(self):
        if len(self.card_showcase_data_list) < 8 or not any(card["name"] for card in self.card_showcase_data_list):
            print([card['name'] for card in self.card_showcase_data_list])
            self.switch_to_returnable_page.emit(10)
            self.error_message.emit("Deck must have at least 8 cards to be set as current deck.")
            return
        self.set_current_deck.emit(self.deck_name)
        self.switch_to_returnable_page.emit(10)
        self.error_message.emit("Deck has been set as current deck.")

    def refresh_after_delete(self):
        # Remove empty entries at the end of the list
        while self.card_showcase_data_list and self.card_showcase_data_list[-1]["name"] == "":
            self.card_showcase_data_list.pop()
            
        # Refresh all cards
        for card_showcase in self.card_showcase_list:
            card_showcase.refresh_card()
        
    def refresh_page(self):
        # First disconnect all signals
        for card_showcase in self.card_showcase_list:
            try:
                card_showcase.leftClicked.disconnect()
                card_showcase.rightClicked.disconnect()
            except TypeError:
                pass

        # Then update and reconnect
        for i, card_showcase in enumerate(self.card_showcase_list):
            if i < len(self.card_showcase_data_list):
                card_data = self.card_showcase_data_list[i]
                card_showcase.set_card_name(card_data["name"])
                # card_showcase.set_card_name(card_data.name)
                card_showcase.image_path = card_data["image_path"] if card_data["name"] else ""
                if card_data["name"]:  # Only connect if the card has a name
                # if card_data.name:  # Only connect if the card has a name
                #     # card_showcase.image_path = card_data.image_path
                #     card_showcase.image_path = "GUI/BattlePage/Afallen.jpg"
                    card_showcase.leftClicked.connect(self.on_card_right_clicked)
                    card_showcase.rightClicked.connect(self.delete_card_showcase)
            else:
                card_showcase.set_card_name("")
                card_showcase.image_path = ""
            card_showcase.refresh_card()

    def save_card_deck(self):
        card_list = []
        for card in self.card_showcase_data_list:
            card_list.append(card.get("name"))
        deck_name = self.current_deck_name if self.current_deck_name else f"Deck {len(self.deck.deck_list)+1}"
        data = {
            "deck_name": deck_name,
            "cards": card_list
        }
        self.save_deck.emit(data)
        self.current_deck_name = ""
    
    # def set_as_current_deck(self):
    #     deck_name = self.current_deck_name 
    #     self.set_current_deck.emit(deck_name)
    # def save_deck(self,dictionary,deck_stage):
    #     with open("Data/CardDeckRecord.json", "w", encoding="utf-8") as f:
    #         json.dump(dictionary, f, ensure_ascii=False, indent=4)
    #     deck_stage.deck_list.append(dictionary)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.RightButton:
    #         self.clicked.emit(self.id)
    #     if event.button() == Qt.LeftButton:
    #         self.clicked.emit(18)

class ConfirmationPage(QWidget):
    switch_to_page = pyqtSignal(int)
    send_card_name = pyqtSignal(str)
    def __init__(self,deck=DeckStage()):
        super().__init__()
        self.deck_stage = deck
        self.card_name = ""
        self.label = QLabel(f"Are you sure to add {self.card_name} into {self.deck_stage.current_deck_name} deck?")
        self.label.setStyleSheet("font-size: 30px;")

        self.yesButton = QPushButton("Yes")
        self.yesButton.setMaximumSize(100,100)
        self.yesButton.clicked.connect(self.on_click_yes)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.on_click_cancel)
        self.cancelButton.setMaximumSize(100,100)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.yesButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.cancelButton)

        confirmationLayout = QVBoxLayout()
        confirmationLayout.addWidget(self.label)
        confirmationLayout.addLayout(buttonLayout)

        #self.background = QLabel()
        #self.background.setMaximumSize(600,200)
        #self.background.setStyleSheet()
        #self.background.setLayout(confirmationLayout)
        page_layout = QGridLayout(self)
        #page_layout.addWidget(self.background,1,1)
        page_layout.addLayout(confirmationLayout,1,1)
        page_layout.setRowStretch(0,1)
        page_layout.setRowStretch(2,1)
        page_layout.setColumnStretch(0,1)
        page_layout.setColumnStretch(2,1)

    def on_click_cancel(self):
        self.switch_to_page.emit(5)
    
    def on_click_yes(self):
        # self.deck_stage.add_card(self.card_name)
        self.send_card_name.emit(self.card_name)
    
    def refresh_label(self, card_name):
        self.card_name = card_name
        self.label.setText(f"Are you sure to add {self.card_name} into {self.deck_stage.current_deck_name} deck?")

class Message_Page(QWidget):
    switch_to_page = pyqtSignal(int)
    def __init__(self, message=""):
        super().__init__()
        self.message = message
        self.label = QLabel(self.message)
        self.label.setStyleSheet("font-size: 30px;")

        self.okButton = QPushButton("OK")
        self.okButton.setMaximumSize(100,100)
        self.okButton.clicked.connect(self.on_click_ok)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)

        messageLayout = QVBoxLayout()
        messageLayout.addWidget(self.label)
        messageLayout.addLayout(buttonLayout)

        page_layout = QGridLayout(self)
        page_layout.addLayout(messageLayout,1,1)
        page_layout.setRowStretch(0,1)
        page_layout.setRowStretch(2,1)
        page_layout.setColumnStretch(0,1)
        page_layout.setColumnStretch(2,1)

    def on_click_ok(self):
        self.switch_to_page.emit(8)
    
    def set_message(self, message):
        self.message = message
        self.label.setText(self.message)

    def clear_message(self):
        self.message = ""
        self.label.setText(self.message)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CreateDeckPage()
    #window = CardDetailPage("name", "descripton")
    window.show()
    sys.exit(app.exec_())