from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel,QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))
from Card.BattleContent import *
from Card.Effect import *
from GUI.BattlePage.show_enemy_page import *

class PlayerPage(EnemyPage):
    def __init__(self, battle):
        super().__init__(battle)
        # self.title_label.setText("Player Info")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo_battle = BattleContent()
    player_page = PlayerPage(demo_battle)
    player_page.show()
    sys.exit(app.exec_())