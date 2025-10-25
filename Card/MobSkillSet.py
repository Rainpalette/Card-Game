from Card.CardEffect import * 
#from BossSkillSetting import BossSkillSetting
import random
import time
from abc import ABC,abstractmethod



class BossSkillSetting(ABC):
    def __init__(self, name, mana_cost, description,battle_content):
        self.name = name
        self.mana_cost = mana_cost
        self.description = description
        self.battle = battle_content
        self.repeatable = 5
        self.max_repeatable = 5
    
    @abstractmethod
    def skill_effect(self):
        pass

effect = CardEffect()
class MobSkillSet:
    def __init__(self, name):
        self.name = name
    # def damage(self, player, damage):
    #     player.health -= damage
    # def heal(self, mob, heal):
    #     mob.health += heal
    # def shield(self, mob, shield):
    #     mob.shield += shield


class RadielSkillSet:
    def __init__(self, battle):
        self.battle = battle

    def handle_skill(self):
        if self.battle.mob.mana < 1:
            # Add logic for when mana is less than 1
            pass
        else:
            # Add logic for when mana is sufficient
            pass

    def attack(self):
        # Uses mana: 2
        self.battle.mob.mana -= 2
        self.battle.player.health -= 6

    def increase_mana(self):
        # Uses mana: 3
        self.battle.mob.mana -= 3
        self.battle.mob.max_mana += 1

    def gain_shield(self):
        # Uses mana: 2
        self.battle.mob.mana -= 2
        self.battle.mob.shield += 10

class crownAttack(BossSkillSetting):
    def __init__(self,battle_content):
        super().__init__("attack", 1, "Deals 2 damage to player", battle_content)
    
    def skill_effect(self):
        effect.deal_damage_to_player(2, self.battle)
        self.battle.mob.mana -=1   

class IncreaseManaSkill(BossSkillSetting):
    def __init__(self, battle_content):
        super().__init__("increaseMana", 1, "Increase max mana by 1", battle_content)
        self.max_repeatable =2
        self.repeatable =2

    def skill_effect(self):
        self.battle.mob.max_mana += 1
        self.battle.mob.mana -= self.mana_cost
        

class GrabShieldSkill(BossSkillSetting):
    def __init__(self,battle_content):
        super().__init__("grabShield", 3, "Steal player's shield and gain your own", battle_content)

    def skill_effect(self):
        mob = self.battle.mob
        player = self.battle.player
        mob.shield += 3
        if player.shield > 5:
            player.shield -= 5
            mob.shield += 5
        elif player.shield>0 and player.shield<=5:
            player.shield =0
            mob.shield +=5
        mob.mana -= self.mana_cost

class CriticalAttackSkill(BossSkillSetting):
    def __init__(self,battle_content):
        super().__init__("criticalAttack", 1, "Ignores shield and deals 3 damage", battle_content)

    def skill_effect(self):
        effect.deal_damage_to_player_ignore_shield(3, self.battle)
        self.battle.mob.mana -= self.mana_cost

class DoNothingSkill(BossSkillSetting):
    def __init__(self,battle_content):
        super().__init__("doNothing", 1, "Do nothing", battle_content)

    def skill_effect(self):
        self.battle.mob.mana -= self.mana_cost

class MagicalAttackSkill(BossSkillSetting):
    def __init__(self,battle_content):
        super().__init__("magicalAttack", 2, "Deal 1 damage and increase max mana by 1", battle_content)

    def skill_effect(self):
        effect.deal_damage_to_player(1, self.battle)
        self.battle.mob.max_mana += 1
        self.battle.mob.mana -= self.mana_cost


class EatSkill(BossSkillSetting):
    def __init__(self,battle_content):
        super().__init__("eat", 0, "Recover 1 health and 1 mana", battle_content)
        self.max_repeatable = 1
        self.repeatable = 1

    def skill_effect(self):
        self.battle.mob.health += 1
        self.battle.mob.mana += 1
    
    



class crownSkillSet:
    def __init__(self, battle):
        self.battle = battle
        self.currrent_skill = None
        self.skill_in_this_round = []
        self.skills = [
            crownAttack(self.battle),
            IncreaseManaSkill(self.battle),
            GrabShieldSkill(self.battle),
            CriticalAttackSkill(self.battle),
            DoNothingSkill(self.battle),
            MagicalAttackSkill(self.battle),
            EatSkill(self.battle)
        ]
    def reset_repeatable(self):
        for skill in self.skills:
            skill.repeatable = skill.max_repeatable
    
    def get_available_skills(self):
        #mana = min(self.battle.mob.mana, 3)
        skill_list =[]
        for skill in self.skills:
            if skill.mana_cost<=self.battle.mob.mana:
                skill_list.append(skill)
        return skill_list
    
    def choose_and_use_skill(self):
        available = self.get_available_skills()
        if not available:
            return None
        
        # while True:
        #     skill = random.choice(available)
        #     if skill.repeatable <=0:
        #         continue
        #     else:
        #         skill.repeatable -=1
        #         break

        # skill.skill_effect(self.battle)
        # self.currrent_skill = skill.name
        # self.skill_in_this_round.append(skill.name)
        # return self.currrent_skill

        for _ in range(10):
            skill = random.choice(available)
            if self.battle.player.shield >0 and self.skills[2].repeatable>0:
                skill = self.skills[2]
            elif self.battle.mob.mana>8:
                attack = [self.skills[0],
                          self.skills[3],
                          self.skills[5]
                          ]
                skill = random.choice(attack)
            if skill.repeatable<=0:
                continue
            skill.repeatable -=1
            try:
                skill.skill_effect()
            except Exception as e:
                print(f"[ERROR] Skill {skill.name} failed: {e}")
                continue
            
            self.currrent_skill = skill.name
            self.skill_in_this_round.append(skill.name)
            return self.currrent_skill
    # def handle_skill(self):
        # while True:
        #     if self.battle.mob.mana >0:
        #         self.choose_and_use_skill()
        #         time.sleep(0.6)
        #     else:
        #         return False
        


    # def attack(self):
    #     self.currrent_skill = self.name
    #     self.skill_in_this_round.append(self.name)
    
    # def increaseMana(self):
    #     self.battle.mob.maxmana +=1
    #     self.battle.mob.mana -=2
    #     self.currrent_skill = "increaseMana"
    #     self.skill_in_this_round.append("increaseMana")
    
    # def grabShield(self):
    #     self.battle.mob.shield +=3
    #     if self.battle.player.shield > 0:
    #         self.battle.player.shield -=5
    #         self.battle.mob.shield +=5
    #     self.battle.mob.mana -=3
    #     self.currrent_skill = "grabShield"
    #     self.skill_in_this_round.append("grabShield")
    
    # def criticalAttack(self):
    #     effect.deal_damage_to_player_ignore_shield(3,self.battle)
    #     self.battle.mob.mana -=1
    #     self.currrent_skill = "criticalAttack"
    #     self.skill_in_this_round.append("criticalAttack")
    
    # def doNothing(self):
    #     self.battle.mob.mana -=1
    #     self.currrent_skill = "doNothing"
    #     self.skill_in_this_round.append("doNothing")
    
    # def magicalAttack(self):
    #     effect.deal_damage_to_player(1, self.battle)
    #     self.battle.mob.maxmana +=1
    #     self.battle.mob.mana -=2
    #     self.currrent_skill = "magicalAttack"
    #     self.skill_in_this_round.append("magicalAttack")

    # def eat(self):
    #     self.battle.mob.health +=1
    #     self.battle.mob.mana +=1
    #     self.currrent_skill = "eat"
    #     self.skill_in_this_round.append("eat")
    
    # def return_skill(self, choice):
    #     return choice
    
    # def handle_skill(self):
    #     mana = self.battle.mob.mana
    #     if mana > 3:
    #         mana = 3
    #     skill_pool = {
    #         3: [self.attack, self.increaseMana, self.grabShield, self.criticalAttack, 
    #             self.doNothing, self.magicalAttack, self.eat],
    #         2: [self.attack, self.increaseMana, self.criticalAttack, self.doNothing, 
    #             self.magicalAttack, self.eat],
    #         1: [self.attack, self.criticalAttack, self.doNothing, self.eat]
    #     }

    #     available_skills = skill_pool.get(mana, [])
        

    #     skill = random.choice(available_skills)
    #     skill()




    

        
    
