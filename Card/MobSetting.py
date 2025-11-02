from abc import ABC, abstractmethod
from Card.MobSkillSet import *

class MobSetting(ABC):
    def __init__(self, name="", health=0, mana=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.before_change_health = health
        self.mana = mana
        self.max_mana = mana
        self.maximal_mana = 10
        self.shield = 0
        self.shield_before_change = 0
        self.effects = []
        self.defense = 0
        self.attack = 0

    def add_effect(self, effect):
        for existing_effect in self.effects:
            if existing_effect.name == effect.name and existing_effect.stackable:
                existing_effect.stack += effect.stack
                return
        self.effects.append(effect)

    def add_multiple_effect(self, effect, stack):
        effect.stack = stack
        self.effects.append(effect)

    def remove_effect(self, effect):
        if effect in self.effects:
            self.effects.remove(effect)
        print(f"Effect {effect.name} removed from mob {self.name}")

    def get_effects(self):
        effect_list = []
        for effect in self.effects:
            effect_list.append(effect)
        return effect_list

    @abstractmethod
    def use_skill(self):
        pass

class crown(MobSetting):
    #crownSkill = crownSkillSet()
    def __init__(self, battle):
        super().__init__("Crown", 100, 5)
        self.battle = battle
        self.crownSkill = None
    
    def setup(self):
        self.crownSkill = crownSkillSet(self.battle)
    
    def use_skill(self):
        #self.crownSkill.handle_skill(self.battle)
        skill_name = self.crownSkill.choose_and_use_skill()
        return skill_name
    def reset_skill(self):
        self.crownSkill.reset_repeatable()
    
    def get_skill_name(self,index):
        return self.crownSkill.skills[index]
        
