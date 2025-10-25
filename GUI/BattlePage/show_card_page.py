from PyQt5.QtWidgets import QApplication, QWidget,QGraphicsOpacityEffect, QGridLayout,QTextEdit, QScrollArea,QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from functools import partial
import json


class Card(QWidget):
    leftClicked = pyqtSignal(int)
    rightClicked = pyqtSignal(str)
    def __init__(self, name="", image_path=""):
        super().__init__()
        self.setAutoFillBackground(True)
        # self.setText(name)
        layout = QVBoxLayout()
        # card_icon = QIcon(image_path)
        # self.setIcon(card_icon)
        # layout.addWidget(self.setText(name))
        # layout.addWidget(card_icon)
        # self.setLayout(layout)
        self.name = name
        self.image_path = image_path
        self.pixmap = QPixmap(self.image_path).scaled(150,350,Qt.KeepAspectRatio)
        self.card_name = QLabel(self.name)
        self.card_name.setAlignment(Qt.AlignCenter)
        self.card_image = QLabel()
        self.card_image.setPixmap(self.pixmap)
        self.card_image.setAlignment(Qt.AlignCenter)
        self.id =0
        self.setFixedSize(200,250)
        self.card = QWidget()
        self.card.setStyleSheet("background-color: #C19A6B;")
        
        layout.addWidget(self.card_name)
        layout.addWidget(self.card_image)
        self.card.setStyleSheet("""
            QWidget{
                border-radius: 8px;
                border: 2px solid #8b5a2b;
                                }""")
        self.card.setLayout(layout)
        
        card_layout = QVBoxLayout(self)
        card_layout.addWidget(self.card)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #caa472;
                
            }
            QWidget:hover {
                background-color: #d4b483;
                
            }
        """)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftClicked.emit(self.id)
        elif event.button() == Qt.RightButton:
            self.rightClicked.emit(self.name)
    
    def in_cooldown(self):
        #self.setWindowOpacity(0.5)
        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.5))
    
    def cooldown_end(self):
        #self.setWindowOpacity(1.0)
        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
    def refresh_card(self):
        self.card_name.setText(self.name)
        self.pixmap = QPixmap(self.image_path).scaled(150,350,Qt.KeepAspectRatio)
        self.card_image.setPixmap(self.pixmap)
            
        #self.setStyleSheet("border: 1px solid black; padding: 5px; background-color: brown;")
        # self.setStyleSheet("""
        #     QWidget {
        #         border: 2px solid black;
        #         border-radius: 10px;
        #         background-color: brown;
        #     }
        #     QLabel {
        #         background: transparent;
        #     }
        # """)

class CardGridWindow(QWidget):
    switch_to_page = pyqtSignal(int)
    send_id = pyqtSignal(int)
    send_name = pyqtSignal(str)
    def __init__(self,deck):
        super().__init__()
        #self.setWindowTitle("Card Grid Layout")
        self.card_gallery =[]
        grid = QGridLayout(self)
        exit_button = QPushButton("Back")
        exit_button.setFixedSize(50,50)
        exit_button.clicked.connect(self.on_click_exit_deck)
        grid.addWidget(exit_button,0,0)
        
        card_count = 0
        for row in range(3):
            for col in range(4):
                if card_count<8:
                    card = Card(deck.get_card_name(card_count), "GUI/BattlePage/Afallen.jpg")
                    card.id = card_count+1
                    card.rightClicked.connect(self.on_card_clicked)
                    card.leftClicked.connect(self.use_card)
                    grid.addWidget(card, row+1, col+1)
                    self.card_gallery.append(card)
                    card_count +=1
                else:
                    card = Card("name", "GUI/BattlePage/Afallen.jpg")
                    card.id = card_count+1
                    card.rightClicked.connect(self.on_card_clicked)
                    grid.addWidget(card, row+1, col+1)
                    card_count +=1

        
        grid.setRowStretch(0,1)
        grid.setRowStretch(4,1)

        #grid.setColumnStretch(0,1)
        #grid.setColumnStretch(5,1)
    
    def on_click_exit_deck(self):
        self.switch_to_page.emit(1)
    
    def on_card_clicked(self, name):
        self.send_name.emit(name)
    
    def use_card(self, id):
        self.send_id.emit(id)

class CardDetailPage(QWidget):
    switch_to_page = pyqtSignal(int)
    change_to_page = pyqtSignal(int)
    def __init__(self,name="", description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.card_name = QLabel(self.name)
        self.card_name.setStyleSheet("font-size:30px;")
        #self.card_name.setFixedSize(100,50)

        self.card_image = QLabel()
        pixmap = QPixmap("GUI/BattlePage/Afallen.jpg")
        self.card_image.setPixmap(pixmap)
        self.card_image.setFixedSize(250,300)

        self.card = QWidget()
        self.card.setStyleSheet("background-color: #C19A6B;")
        card_layout = QVBoxLayout()
        card_layout.addWidget(self.card_name)
        card_layout.addWidget(self.card_image)
        self.card.setLayout(card_layout)
        
        # with open("GUI/BattlePage/radiel_description.txt", "r", encoding="utf-8") as f:
        #     description_text = f.read()

        # with open(r"Data\Card.json", "r", encoding="utf-8") as f:
        #     cards = json.load(f)
        page_layout = QGridLayout(self)
        self.card_description = QTextEdit()
        self.card_description.setReadOnly(True)
        #self.card_description.setPlainText(description_text)
        self.card_description.setPlainText(self.description)
        self.card_description.setFixedWidth(500)
        #self.card_description.setWordWrap(True)
        # self.scroll_area = QScrollArea()
        # self.scroll_area.setWidget(self.card_description)
        #self.scroll_area.setMaximumWidth(500)
        page_layout.addWidget(self.card,2,2)
        page_layout.setRowStretch(1,1)
        page_layout.setRowStretch(3,1)
        page_layout.setColumnStretch(1,1)
        page_layout.setColumnStretch(4,1)
        page_layout.addWidget(self.card_description,2,3)

        exit_button = QPushButton("Back")
        exit_button.setFixedSize(50,50)
        exit_button.clicked.connect(self.on_click_exit_deck)
        page_layout.addWidget(exit_button,0,0)
    
    def on_click_exit_deck(self):
        self.change_to_page.emit(3)
    
    def refresh_page(self):
        self.card_name.setText(self.name)
        self.card_description.setPlainText(self.description)






    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CardGridWindow()
    #window = CardDetailPage("name", "descripton")
    window.show()
    sys.exit(app.exec_())