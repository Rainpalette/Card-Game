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
        # self.enemy_health_bar = QLabel()
        # self.enemy_health_bar.setText(f"{self.battle.mob.health} ({self.battle.mob.shield}) mana:{self.battle.mob.mana}")
        # self.enemy_health_bar.setStyleSheet("""font-size: 25px;
        #                                     color: #c6c6e8""")
        
        # Create enemy image button
        self.enemy_image = QPushButton()
        self.enemy_icon = QIcon("Clown.png")
        self.enemy_image.setFixedSize(200, 200)

        # Make button background transparent
        self.enemy_image.setStyleSheet("""
                QPushButton {
                    background-color: #b3bfcb;
                    border: 3px solid #313c45;
                    border-radius: 5px;
                    font-size: 70px;
                }
                QPushButton:hover {
                    border: 3px solid #3d4a54;
                    background-color: #c0cbd5;
                }
                QLabel {
                        font-size: 70px;
                        color: #FF4444;
                    }
                """)
        self.enemy_image.setIcon(self.enemy_icon)
        self.enemy_health_bar = QLabel(self.enemy_image)
        self.enemy_health_bar.move(160,-10)
        self.enemy_health_bar.setFixedSize(50,50)
        self.enemy_health_bar.setText(f"{self.battle.mob.health}")
        self.enemy_health_bar.setStyleSheet("""font-size: 40px;
                                             background-color: transparent;
                                             font-weight: bold;
                                             color: #344979;
                                            """)
        self.enemy_shield_bar = QLabel(self.enemy_image)
        self.enemy_shield_bar.move(0,-10)
        self.enemy_shield_bar.setFixedSize(50,50)
        self.enemy_shield_bar.setText(f"{self.battle.mob.shield}")
        self.enemy_shield_bar.setStyleSheet("""font-size: 40px;
                                             background-color: transparent;
                                             font-weight: bold;
                                             color: #344979;
                                            """)
        # Create damage label that will overlay the image
        self.enemy_damage_label = QLabel("5", self.enemy_image)  # Make it a child of enemy_image
        self.enemy_damage_label.setStyleSheet("""
            QLabel {
                font-size: 70px;
                color: #FF4444;
            }
        """)
        self.enemy_damage_label.setFixedSize(80,60)
        # Position the label at the top-right corner of the image
        self.enemy_damage_label.move(80,80)  # Adjust these values to position the label
        self.enemy_damage_label.hide()

        self.enemy_name = QLabel(self.battle.mob.name)
        self.enemy_name.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.enemy_skill_name = QLabel()
        self.enemy_skill_name.setStyleSheet("font-size: 30px; font-weight: bold;")
        # dynamic_enemy_layout.addWidget(self.enemy_image, alignment=Qt.AlignCenter)
        # dynamic_enemy_layout.addWidget(self.enemy_damage_label, alignment=Qt.AlignLeft)
        self.enemy_image.clicked.connect(self.on_click_enemy_profile)
        self.enemy_image.setIconSize(QSize(200,200))
        #enemy_image.setScaledContents(True)  
        # self.enemy_damage_label = QLabel("0")
        # self.enemy_damage_label.hide()
        # self.enemy_damage_label.setStyleSheet("font-size: 20px;")

        # enemy_layout.addWidget(self.enemy_health_bar, alignment=Qt.AlignCenter)
        # enemy_layout.addLayout(dynamic_enemy_layout, Qt.AlignCenter)
        enemy_layout.addWidget(self.enemy_image, alignment=Qt.AlignCenter)
        enemy_layout.addWidget(self.enemy_name, alignment=Qt.AlignCenter)
        enemy_layout.addWidget(self.enemy_skill_name, alignment=Qt.AlignCenter)
        # enemy_layout.addWidget(self.enemy_damage_label, alignment=Qt.AlignCenter)

        # dynamic_enemy_layout = QHBoxLayout()
        # self.enemy_damage_label = QLabel("Damage: 0")
        # self.enemy_damage_label.setStyleSheet("font-size: 20px;")
        
        # dynamic_enemy_layout.addLayout(enemy_layout, Qt.AlignCenter)
        # dynamic_enemy_layout.addWidget(self.enemy_damage_label, alignment=Qt.AlignLeft)
        # self.main_layout.addLayout(dynamic_enemy_layout, 0, 1)
        self.main_layout.addLayout(enemy_layout, 0, 1)
        #game_detial_layout = QVBoxLayout()
        self.round_label = QLabel("Round 1")
        self.round_label.setStyleSheet("font-size: 30px; font-weight: bold;color:#778ca4;")

        self.enemy_mana_bar = QLabel()
        self.enemy_mana_bar.setText(f"Mana remaining:\n             {self.battle.mob.mana}")
        self.enemy_mana_bar.setStyleSheet("font-size: 30px;font-weight: bold;color:#c6c6e8;")
        self.main_layout.addWidget(self.round_label, 1, 0, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.enemy_mana_bar,0,2,alignment=Qt.AlignCenter)
        #self.player_mana_bar = Manabar()
        self.player_mana_bar = QLabel()
        self.player_mana_bar.setText(f"Mana remaining:\n             {self.battle.player.mana}")
        self.player_mana_bar.setStyleSheet("font-size: 25px;")
        self.main_layout.addWidget(self.player_mana_bar,2,0,alignment=Qt.AlignCenter)
        
        player_layout = QVBoxLayout()
        self.player_image = QPushButton()  # Made this a class attribute so we can reference it
        self.player_image.setFixedSize(200,200)
        # Make button background transparent
        self.player_image.setStyleSheet("""
            QPushButton {
                background-color: #b3bfcb;
                border: 3px solid #313c45;
                border-radius: 5px;
            }
            QPushButton:hover {
                border: 3px solid #3d4a54;
                background-color: #c0cbd5;
            }
            QLabel {
                font-size: 70px;
                color: #FF4444;
            }
        """)
        player_icon = QIcon("Player_Metris.png")
        self.player_image.setIcon(player_icon)
        self.player_image.setIconSize(QSize(200,200))
        
        # Create damage label that will overlay the player image
        self.player_damage_label = QLabel("5", self.player_image)  # Make it a child of player_image
        self.player_damage_label.setStyleSheet("""
            QLabel {
                font-size: 70px;
                color: #FF4444;
            }
        """)
        self.player_damage_label.setFixedSize(80,60)
        # Position the label at the top-right corner of the image
        self.player_damage_label.move(80,80)  # Same position as enemy damage label
        self.player_damage_label.hide()

        # self.player_health_bar = QLabel(f"{self.battle.player.health} ({self.battle.player.shield})")
        self.player_health_bar = QLabel(self.player_image)
        self.player_health_bar.move(160,-10)
        self.player_health_bar.setText(f"{self.battle.player.health}")
        self.player_health_bar.setStyleSheet("""font-size: 40px;
                                             background-color: transparent;
                                             font-weight: bold;
                                             color: #344979;
                                            """)
        self.player_shield_bar = QLabel(self.player_image)
        self.player_shield_bar.move(0,-10)
        self.player_shield_bar.setText(f"{self.battle.player.shield}")
        self.player_shield_bar.setStyleSheet("""font-size: 40px;
                                             background-color: transparent;
                                             font-weight: bold;
                                             color: #344979;
                                            """)


        self.player_skill_name = QLabel()
        self.player_skill_name.setStyleSheet("font-size: 30px; font-weight: bold;")
        player_layout.addWidget(self.player_skill_name, alignment=Qt.AlignCenter)
        player_layout.addWidget(self.player_image, alignment=Qt.AlignCenter)  # Updated to use self.player_image
        # player_layout.addWidget(self.player_health_bar, alignment=Qt.Align)
        self.main_layout.addLayout(player_layout, 2, 1)

        #Add card deck into the widget
        self.player_card_deck = QPushButton()  # Remove text and background image
        self.player_card_deck.setFixedSize(120,150)
        card_icon = QIcon("Card_icon.jpg")
        self.player_card_deck.setIcon(card_icon)
        self.player_card_deck.setIconSize(QSize(110, 140))  # Slightly smaller than button size
        self.player_card_deck.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 3px solid #313c45;
                border-radius: 5px;
            }
            QPushButton:hover {
                border: 3px solid #3d4a54;
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.player_card_deck.clicked.connect(self.on_click_card_deck)
        
        self.main_layout.addWidget(self.player_card_deck,2,2,alignment=Qt.AlignTop)
        

        #Add Round End button into the widget
        self.player_end_button = QPushButton("Round End")
        self.player_end_button.setFixedSize(200,200)
        # self.player_end_button.setStyleSheet("font-size:30px;")
        self.player_end_button.setStyleSheet("""
            QPushButton {
                font-size: 30px;
                border-radius: 10px;
                border: 3px solid black;
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
        self.player_mana_bar.setText(f"Mana remaining:\n             {self.battle.player.mana}")
        self.player_mana_bar.setStyleSheet("color:#778CA4;font-weight: bold;font-size: 30px;")
        self.enemy_health_bar.setText(f"{self.battle.mob.health}")
        self.enemy_shield_bar.setText(f"{self.battle.mob.shield}")
        self.enemy_mana_bar.setText(f"Mana remaining:\n             {self.battle.mob.mana}")
        self.player_health_bar.setText(f"{self.battle.player.health}")
        self.player_shield_bar.setText(f"{self.battle.player.shield}")
        count =0
        for card in deck:
            if card.current_cooldown <=0:
                page.card_gallery[count].cooldown_end()
            count+=1
    
    def update_round(self, round_number):
        self.round_label.setText(f"Round {round_number}")

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
    
    def show_damage_on_enemy(self,damage):
        #if the damage is negative, it means healing
        #get the absolute value of damage and return it
        print(f"shield before: {self.battle.mob.shield_before_change}")
        print(f"shield after: {self.battle.mob.shield}")
        print(f"Damage to show: {damage}")
        if damage<0:
            damage = abs(damage)
            print(f"Healing detected: {damage}")
            self.enemy_damage_label.setText(str(damage))
            self.enemy_damage_label.setStyleSheet("color: green;")
            self.enemy_damage_label.show()
            print(f"Healing shown: {damage}")
            self.battle.mob.before_change_health = self.battle.mob.health
            self.battle.mob.shield_before_change = self.battle.mob.shield
        elif damage>0:
            self.enemy_damage_label.setStyleSheet("color: red;")
            self.enemy_damage_label.setText(str(damage))
            self.enemy_damage_label.show()
            self.battle.mob.before_change_health = self.battle.mob.health
            self.battle.mob.shield_before_change = self.battle.mob.shield
        
        elif damage==0 and self.battle.mob.shield>0 and self.battle.mob.shield_before_change>self.battle.mob.shield:
            self.enemy_damage_label.setStyleSheet("color: gray;")
            self.enemy_damage_label.setText(str(damage))
            self.enemy_damage_label.show()
            self.battle.mob.before_change_health = self.battle.mob.health
            self.battle.mob.shield_before_change = self.battle.mob.shield
        elif damage==0 and self.battle.mob.shield==0 and self.battle.mob.shield_before_change>0:
            self.enemy_damage_label.setStyleSheet("color: gray;")
            self.enemy_damage_label.setText(str(damage))
            self.enemy_damage_label.show()
            self.battle.mob.before_change_health = self.battle.mob.health
            self.battle.mob.shield_before_change = self.battle.mob.shield
        
    
    def show_damage_on_player(self,damage):
        #if the damage is negative, it means healing
        #get the absolute value of damage and return it
        if damage<0:
            damage = abs(damage)
            print(f"Healing detected: {damage}")
            self.player_damage_label.setText(str(damage))
            self.player_damage_label.setStyleSheet("color: green;")
            self.player_damage_label.show()
            self.battle.player.before_change_health = self.battle.player.health
            print(f"Healing shown: {damage}")
        elif damage>0:
            self.player_damage_label.setStyleSheet("color: red;")
            self.player_damage_label.setText(str(damage))
            self.player_damage_label.show()
            self.battle.player.before_change_health = self.battle.player.health
        elif damage==0 and self.battle.player.shield>0 and self.battle.player.shield_before_change>self.battle.player.shield:
            self.player_damage_label.setStyleSheet("color: gray;")
            self.player_damage_label.setText(str(damage))
            self.player_damage_label.show()
            self.battle.player.before_change_health = self.battle.player.health
            self.battle.player.shield_before_change = self.battle.player.shield
        elif damage==0 and self.battle.player.shield==0 and self.battle.player.shield_before_change>0:
            self.player_damage_label.setStyleSheet("color: gray;")
            self.player_damage_label.setText(str(damage))
            self.player_damage_label.show()
            self.battle.player.before_change_health = self.battle.player.health
            self.battle.player.shield_before_change = self.battle.player.shield
        
class ChooseEnemyProfile(QWidget):
    def __init__(self,battle):
        super().__init__()
        self.battle = battle
        self.main_layout = QVBoxLayout(self)
        self.profile_label = QLabel("Enemy Profile")
        self.pixmap = QPixmap("GUI/BattlePage/Afallen.jpg").scaled(300,300,Qt.KeepAspectRatio)
        self.profile_image = QLabel()
        self.profile_image.setPixmap(self.pixmap)
        self.profile_image.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.profile_label)
        self.main_layout.addWidget(self.profile_image)
        self.setLayout(self.main_layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)   # 创建应用实例
    window = BattleBoard()          # 创建主窗口对象
    window.show()                  # 显示窗口
    sys.exit(app.exec_())          # 进入事件循环
