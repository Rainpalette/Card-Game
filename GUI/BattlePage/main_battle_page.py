from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor



import sys
#battle_function = BattleStage()
class Healbar(QLabel):
    def __init__(self,parent=None):
        super().__init__(parent)
        #self.setText("这是一个绘图Label")
        self.rect_color = QColor("red")
        self.setFixedSize(250,50)
        self.text = ""
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        painter.setBrush(self.rect_color)
        painter.setPen(QColor(0,0,0))
        painter.drawRect(20,20,200,30)

        painter.setPen(QColor(255,255,255))
        painter.setFont(self.font())

        rect = self.rect()
        painter.drawText(20, 20, 200,30, Qt.AlignCenter, self.text)

    def set_text(self, string):
        self.text = string

class Manabar(QLabel):
    def __init__(self,parent=None):
        super().__init__(parent)
        #self.setText("这是一个绘图Label")
        self.rect_color = QColor("blue")
        self.setFixedSize(250,50)
        self.text = ""
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        painter.setBrush(self.rect_color)
        painter.setPen(QColor(0,0,0))
        painter.drawRect(20,20,200,30)

        painter.setPen(QColor(255,255,255))
        painter.setFont(self.font())

        rect = self.rect()
        painter.drawText(20, 20, 200,30, Qt.AlignCenter, self.text)
    
    def update_text(self, string):
        self.text = string

class BattleBoard(QWidget):
    switch_to_page = pyqtSignal(int)
    end_turn = pyqtSignal(bool)
    def __init__(self,battle):
        super().__init__()
        self.show_enemy_profile = False
        self.round_end = False
        self.open_card_deck = False
        self.battle = battle

        self.main_layout = QGridLayout(self)

        enemy_layout = QVBoxLayout()
        #self.enemy_health_bar = Healbar()
        self.enemy_health_bar = QLabel()
        self.enemy_health_bar.setText(f"{self.battle.mob.health} ({self.battle.mob.shield}) mana:{self.battle.mob.mana}")
        self.enemy_health_bar.setStyleSheet("font-size: 25px;")
        self.enemy_image = QPushButton()
        self.enemy_icon = QIcon("GUI/BattlePage/Afallen.jpg")
        #self.enemy_name = QLabel("Radiel, Judgment of Injustice")
        self.enemy_name = QLabel(self.battle.mob.name)
        self.enemy_skill_name = QLabel()
        # pixmap = QPixmap("GUI/BattlePage/Afallen.jpg")
        # enemy_image.setPixmap(pixmap)
        self.enemy_image.setFixedSize(200, 200)  
        self.enemy_image.setIcon(self.enemy_icon)
        self.enemy_image.clicked.connect(self.on_click_enemy_profile)
        self.enemy_image.setIconSize(QSize(200,200))
        #enemy_image.setScaledContents(True)  

        enemy_layout.addWidget(self.enemy_health_bar, alignment=Qt.AlignCenter)
        enemy_layout.addWidget(self.enemy_image, alignment=Qt.AlignCenter)
        enemy_layout.addWidget(self.enemy_name, alignment=Qt.AlignCenter)
        enemy_layout.addWidget(self.enemy_skill_name, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(enemy_layout, 0, 1)
        #game_detial_layout = QVBoxLayout()
        round_label = QLabel("Round 1")

        
        self.main_layout.addWidget(round_label, 1, 0, alignment=Qt.AlignCenter)
        #self.player_mana_bar = Manabar()
        self.player_mana_bar = QLabel()
        self.player_mana_bar.setText(str(self.battle.player.mana))
        self.main_layout.addWidget(self.player_mana_bar,2,0,alignment=Qt.AlignCenter)
        
        player_layout = QVBoxLayout()
        player_image = QPushButton()
        #player_pixmap = QPixmap
        #player_image.setPixmap(QPixmap("GUI/BattlePage/D.D.jpg"))
        player_image.setFixedSize(200,200)
        player_icon = QIcon("GUI/BattlePage/D.D.jpg")
        player_image.setIcon(player_icon)
        player_image.setIconSize(QSize(200,200))
        # player_image.setStyleSheet("""
        #         QPushButton{
        #             border: none;
        #             backgrounf-image: url(GUI/BattlePage/D.D.jpg)
        #             background-repeat: no-repeat;
        #             background-position: center;
        #             background-size: cover;     
        #                            }""")
        #player_image.setScaledContents(True)
        self.player_health_bar = QLabel(f"{self.battle.player.health} ({self.battle.player.shield})") # 用图片代替
        self.player_skill_name = QLabel()
        player_layout.addWidget(self.player_skill_name, alignment=Qt.AlignCenter)
        player_layout.addWidget(player_image, alignment=Qt.AlignCenter)
        player_layout.addWidget(self.player_health_bar, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(player_layout, 2, 1)

        #Add card deck into the widget
        self.player_card_deck = QPushButton("Card deck")
        self.player_card_deck.setFixedSize(100,150)
        self.player_card_deck.clicked.connect(self.on_click_card_deck)
        
        self.main_layout.addWidget(self.player_card_deck,2,2,alignment=Qt.AlignTop)
        

        #Add Round End button into the widget
        self.player_end_button = QPushButton("Round End")
        self.player_end_button.setFixedSize(200,200)
        self.player_end_button.setStyleSheet("font-size:30px;")
        self.player_end_button.clicked.connect(self.on_click_end_button)
        self.main_layout.addWidget(self.player_end_button, 1, 2, alignment=Qt.AlignCenter)
       

        self.main_layout.setRowStretch(1, 1)
        self.main_layout.setColumnStretch(1, 1)
    def disable_action(self):
        self.player_end_button.setDisabled(True)
        self.player_card_deck.setDisabled(True)

    def reset_button(self):
        self.player_end_button.setDisabled(False)
        self.player_card_deck.setDisabled(False)
        
    def on_click_end_button(self):
        self.player_end_button.setDisabled(True)
        self.player_card_deck.setDisabled(True)
        self.round_end = True
        self.end_turn.emit(True)
        # battle_function.end_turn(battle_function.card_deck)
        # battle_function.start_turn()


    def update_status(self,deck,page):
        self.enemy_name.setText(self.battle.mob.name)
        self.player_mana_bar.setText(str(self.battle.player.mana))
        self.enemy_health_bar.setText(f"{self.battle.mob.health} ({self.battle.mob.shield}) mana:{self.battle.mob.mana}")
        self.player_health_bar.setText(f"{self.battle.player.health} ({self.battle.player.shield})")
        count =0
        for card in deck:
            if card.current_cooldown <=0:
                page.card_gallery[count].cooldown_end()
            count+=1

                

    def on_click_enemy_profile(self):
        self.show_enemy_profile = True
        self.switch_to_page.emit(3)


    def on_click_card_deck(self):
        self.open_card_deck = True
        self.switch_to_page.emit(2)

    #def end_game_turn(self):
        

    def player_turn(self):
        self.player_end_button.setDisabled(False)
        self.player_card_deck.setDisabled(False)
    
    def Player_use_skill(self,skill_name):
        self.player_skill_name.setText(skill_name)
    
    def clear_skill_label(self):
        self.player_skill_name.setText("")
    
    def boss_use_skill(self,skill_name):
        self.enemy_skill_name.setText(skill_name)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)   # 创建应用实例
    window = BattleBoard()          # 创建主窗口对象
    window.show()                  # 显示窗口
    sys.exit(app.exec_())          # 进入事件循环
