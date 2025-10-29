from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel,QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))
from Card.BattleContent import *

class SkillBar(QWidget):
        def __init__(self, title, description):
            super().__init__()
            #creating skill bar
            self.skill_icon = QLabel("skill")
            self.skill_pixmap = QPixmap("GUI/BattlePage/D.D.jpg")
            self.skill_icon.setPixmap(self.skill_pixmap)
            self.skill_icon.setScaledContents(True)
            self.skill_icon.setFixedSize(85,85)
            self.skill_title = QLabel()
            self.skill_title.setText(title)
            self.skill_title.setStyleSheet("font-size: 30px;")

            

            self.skill_description =QLabel()
            self.skill_description.setText(description)
            self.skill_description.setStyleSheet("font-size: 20px")

            self.skill_description_layout = QVBoxLayout()
            self.skill_description_layout.addWidget(self.skill_title)
            self.skill_description_layout.addWidget(self.skill_description)
            self.skill_description_layout.setStretch(0,2)
            self.skill_description_layout.setStretch(1,1)

            self.skill_bar_layout = QHBoxLayout()
            self.skill_bar_layout.addWidget(self.skill_icon)
            self.skill_bar_layout.addLayout(self.skill_description_layout)

            self.setLayout(self.skill_bar_layout)
            # self.skill_bar = QLabel()
            # self.skill_bar.setLayout(self.skill_bar_layout)

class EffectBar(QWidget):
     def __init__(self, title, description):
        super().__init__()
        # skill = crown['skills']
        # current_skill = skill[0]
        self.name = title
        self.effect_icon = QLabel("Icon")
        self.effect_pixmap = QPixmap("GUI/BattlePage/Afallen.jpg")
        self.effect_icon.setPixmap(self.effect_pixmap)
        self.effect_icon.setScaledContents(True)
        self.effect_icon.setFixedSize(90,90)

        self.effect_title = QLabel()
        self.effect_title.setText(title)
        self.effect_title.setStyleSheet("font-size: 30px;")

        self.effect_description = QLabel()
        self.effect_description.setText(description)
        self.effect_description.setStyleSheet("font-size:20px;")

        self.effect_description_layout = QVBoxLayout()
        self.effect_description_layout.addWidget(self.effect_title)
        self.effect_description_layout.addWidget(self.effect_description)

        self.effect_bar_layout = QHBoxLayout(self)
        self.effect_bar_layout.addWidget(self.effect_icon)
        self.effect_bar_layout.addLayout(self.effect_description_layout)


class EnemyPage(QWidget):
    switch_to_page = pyqtSignal(int)
    
    def __init__(self,battle=BattleContent()):
        super().__init__()
        self.battle = battle
        with open(r"Data\Crown.json", "r", encoding="utf-8") as f:
            boss_data =json.load(f)
        # current_boss = battle.mob.name
        # crown = boss_data.get[current_boss]
        crown = boss_data["Crown"]
        self.page_layout = QHBoxLayout()
        self.boss_detail_layout = QVBoxLayout()
        self.boss_detail = QLabel()
        pixmap = QPixmap(crown['image'])
        self.boss_detail.setPixmap(pixmap)
        self.boss_detail.setFixedSize(200,250)
        self.boss_detail.setScaledContents(True)  # This will make the image scale to fit the label
        self.effect_list = []
        self.update_list = []
        self.boss_name = QLabel()
        self.boss_name.setText(crown['name'])
        self.boss_name.setStyleSheet("font-size: 30px;background-color:black; color:white; padding:5px; border-radius:10px;")

        self.boss_showcase_layout=QVBoxLayout()
        self.boss_showcase_layout.addWidget(self.boss_detail, alignment=Qt.AlignCenter)
        self.boss_showcase_layout.addWidget(self.boss_name, alignment=Qt.AlignCenter)

        self.description = QLabel("Description")
        # with open("GUI/BattlePage/radiel_description.txt", "r", encoding="utf-8") as f:
        #     description_text = f.read()
        # self.description.setText(description_text)
        self.description.setText(crown['description'])
        self.description.setWordWrap(True)
        self.description.setStyleSheet("font-size:20px;")

        self.effect = QLabel("Effect")
        self.effect.setStyleSheet("font-size:35px;")
        self.scroll_area = QScrollArea()

        
            
            
        #creating effect bar
        # skill = crown['skills']
        # current_skill = skill[0]

        # self.effect_icon = QLabel("Icon")
        # self.effect_pixmap = QPixmap("GUI/BattlePage/D.D.jpg")
        # self.effect_icon.setPixmap(self.effect_pixmap)
        # self.effect_icon.setScaledContents(True)
        # self.effect_icon.setFixedSize(90,90)

        # self.effect_title = QLabel()
        # self.effect_title.setText("Title")
        # self.effect_title.setStyleSheet("font-size: 30px;")

        # self.effect_description = QLabel()
        # self.effect_description.setText("some description")
        # self.effect_description.setStyleSheet("font-size:20px;")

        # self.effect_description_layout = QVBoxLayout()
        # self.effect_description_layout.addWidget(self.effect_title)
        # self.effect_description_layout.addWidget(self.effect_description)

        # self.effect_bar_layout = QHBoxLayout()
        # self.effect_bar_layout.addWidget(self.effect_icon)
        # self.effect_bar_layout.addLayout(self.effect_description_layout)

        # self.effect_bar_layout.setStretch(self.effect_icon,stretch=1)
        # self.effect_bar_layout.setStretch(self.effect_description, stretch=2)

        #create scrollable area
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.addWidget(self.description)
        self.scroll_area_layout.addWidget(self.effect)
        if self.battle.mob.effects:
            for effect in self.battle.mob.effects:
                effect_bar = EffectBar(effect.name, effect.description)
                self.scroll_area_layout.addWidget(effect_bar)
                self.scroll_area_layout.addStretch(1)
             
        
        # self.scroll_area_layout.addLayout(self.effect_bar_layout)

        scroll_content = QWidget()
        scroll_content.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(scroll_content)
        self.scroll_area.setWidgetResizable(True)
        #self.scroll_area.setLayout(self.scroll_area_layout)
        for i in range(8):
            effect_bar = EffectBar("", "")
            self.scroll_area_layout.addWidget(effect_bar)
            effect_bar.hide()
            self.effect_list.append(effect_bar)

        # self.boss_detail_layout.addWidget(self.boss_detail)
        # self.boss_detail_layout.addWidget(self.boss_name)
        self.boss_detail_layout.addLayout(self.boss_showcase_layout)
        self.boss_detail_layout.addWidget(self.scroll_area)
        self.boss_detail_layout.setStretch(0,1)
        self.boss_detail_layout.setStretch(1,2)


        self.skill_list_layout = QVBoxLayout()
        self.exit_button = QPushButton("Back")
        self.exit_button.setFixedSize(50,50)
        self.exit_button.clicked.connect(self.on_click_exit_enemy)

        self.skill_list_layout.addWidget(self.exit_button)
        # self.skill_bar = SkillBar()
        # self.skill_list_layout.addWidget(self.skill_bar)
        
        for skill in crown["skills"]:
             skill_bar = SkillBar(skill['name'],skill['description'])
             self.skill_list_layout.addWidget(skill_bar)
             self.skill_list_layout.addStretch(1)
             
        self.skill_scroll_area = QScrollArea()
        skill_content = QWidget()
        skill_content.setLayout(self.skill_list_layout)
        self.skill_scroll_area.setWidget(skill_content)
        self.skill_scroll_area.setWidgetResizable(True)
        self.skill_scroll_area.setLayout(self.skill_list_layout)

        self.page_layout.addWidget(self.skill_scroll_area)
        self.page_layout.addLayout(self.boss_detail_layout)
        self.setLayout(self.page_layout)
    
    def on_click_exit_enemy(self):
        self.switch_to_page.emit(1)

    def update_effect_status(self):
        # effect_bar = EffectBar("name", "description")
        # self.scroll_area_layout.addWidget(effect_bar)
        # print("updating effect status")
        # update_effect = []
        # count = 0
        # print("updating")
        # self.effect_list = self.battle.mob.effects
        # if self.effect_list == []:
        #     print("yyyyyyyyyyyy")
        # else:
        #     print(f"{self.effect_list[0].name}")
        # for effect in self.effect_list:
        #     count =0
        #     print("running through looping")
        #     if not self.update_list:
        #         update_effect = self.effect_list
        #     for term in self.update_list:
        #         if self.update_list and effect.name == self.update_list[count].name:
        #             print("Addition failed")
        #             count+=1
        #             continue
        #         else:
        #             update_effect.append(effect_bar)
        #             print(f"{effect.name} added")
        #             print(term)
        #             count=0
        #             break
        # # print(update_effect[0])
        # # for effect in self.battle.mob.effects:
        # #     print(f"effect name: {effect.name}, description: {effect.description}")
        # for effect in update_effect:
        #     #effect_bar = EffectBar("haha", "Boom")
        #     effect_bar = EffectBar(effect.name, effect.description)
        #     self.scroll_area_layout.addWidget(effect_bar)
        #     #self.effect_list.append(effect_bar)
        #     #self.scroll_area_layout.addStretch(1)
        #     effect_bar.hide()
        # self.update_list = self.battle.mob.effects
        self.update_list = self.battle.mob.effects
        count =0
        hide_count = len(self.update_list)
        if self.update_list == []:
            for effect_bar in self.effect_list:
                effect_bar.hide()
        else:
            for effect in self.update_list:
                self.effect_list[count].effect_title.setText(effect.name)
                self.effect_list[count].effect_description.setText(effect.description)
                self.effect_list[count].effect_pixmap = QPixmap(effect.image_path)
                self.effect_list[count].effect_icon.setPixmap(self.effect_list[count].effect_pixmap)
                self.effect_list[count].show()
                count += 1
            if hide_count < len(self.effect_list):
                self.effect_list[hide_count].hide()
                hide_count += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)   # 创建应用实例
    window = EnemyPage()          # 创建主窗口对象
    window.show()                  # 显示窗口
    sys.exit(app.exec_())          # 进入事件循环            



            



        
        


