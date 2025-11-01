from Card.MobSetting import *
from Card.PlayerSetting import *

class clearMob(MobSetting):
    def __init__(self):
        super().__init__()
        self.name = "clear"
    def use_skill(self):
        return super().use_skill()
    

class BattleContent:
    def __init__(self, mob=clearMob(), player=PlayerSetting()):
        self.mob = mob
        self.player = player
        self.field_effects = []