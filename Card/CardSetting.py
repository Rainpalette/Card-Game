from abc import ABC, abstractmethod
from Card.CardEffect import *


card_effect = CardEffect()
reduce_defense = defenseReduction()
class CardSetting(ABC):
    def __init__(self, name="", mana_cost=0, description="", card_type="", rarity="", cooldown=0, image_path="GUI/Afallen.jpg"):
        self.name = name
        self.mana_cost = mana_cost
        self.description = description
        self.type = card_type
        self.rarity = rarity
        # self.card_effect = card_effect
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.image_path = image_path
        self.background_story = ""
        self.additional_attack = False
        self.activated_times = 0
        self.activate_on_attack = False
        self.effect_on_card = False
        self.effect_on_battle_content = True
        self.activate_on_game_start = False

    @abstractmethod
    def use_card(self, battle):
        pass

    def cooldown_card(self,addition_cooldown=0):
        self.current_cooldown = self.cooldown+addition_cooldown


class NormalAttack(CardSetting):
    def __init__(self):
        super().__init__(
            name="Normal Attack",
            mana_cost=1,
            description="Deal 5 damage to the enemy.",
            card_type="Attack",
            rarity="Common",
            cooldown=3,
            image_path="Card/CardIcon/Sword.png"
        )
        

    def use_card(self, battle):
        card_effect.deal_damage(5,battle)
        

class Heal(CardSetting):
    def __init__(self):
        super().__init__(
            name="Heal",
            mana_cost=1,
            description="Restore 3 HP to yourself.",
            card_type="Heal",
            rarity="Common",
            cooldown=2,
            image_path="Card/CardIcon/heal.png"
        )

    def use_card(self, battle):
        card_effect.heal(3,battle)


class Defense(CardSetting):
    def __init__(self):
        super().__init__(
            name="Defense",
            mana_cost=1,
            description="Gain 3 shield stacks.",
            card_type="Defense",
            rarity="Common",
            cooldown=2,
            image_path="Card/CardIcon/shield.png"
        )

    def use_card(self, battle):
        card_effect.shield(3,battle)


class ShieldCounter(CardSetting):
    def __init__(self):
        super().__init__(
            name="Shield Counter",
            mana_cost=2,
            description="Gain 3 shield stacks and deal 6 damage to the enemy.",
            card_type="Defense",
            rarity="Common",
            cooldown=4
        )

    def use_card(self, battle):
        card_effect.shield(3,battle)
        card_effect.deal_damage(6,battle)


class HolyLight(CardSetting):
    def __init__(self):
        super().__init__(
            name="Holy Light",
            mana_cost=1,
            description="Deal 3 damage, restore 2HP",
            card_type="Effect",
            rarity="Common",
            cooldown=3
        )

    def use_card(self, battle):
        card_effect.deal_damage(3, battle)
        card_effect.heal(2, battle)


class Intimidate(CardSetting):
    def __init__(self):
        super().__init__(
            name="Intimidate",
            mana_cost=1,
            description="Inflict 1 layer of defense reduction on the enemy for 3 turns.",
            card_type="Effect",
            rarity="Common",
            cooldown=3
        )

    def use_card(self, battle):
        #battle.mob.defense -=1
        # battle.mob.add_effect(card_effect.Memory(battle))
        battle.mob.add_effect(defenseReduction())
        reduce_defense.apply_effect(battle)


class CriticalStrike(CardSetting):
    def __init__(self):
        super().__init__(
            name="Critical Strike",
            mana_cost=1,
            description="Deal 8 damage to the enemy.",
            card_type="Attack",
            rarity="Common",
            cooldown=5,
            image_path="Card/CardIcon/Axe.png"
        )

    def use_card(self, battle):
        card_effect.deal_damage(8,battle)


class Trick(CardSetting):
    def __init__(self):
        super().__init__(
            name="Trick",
            mana_cost=2,
            description="Remove the enemy's shield and deal damage equal to the shield value removed.",
            card_type="Effect",
            rarity="Common",
            cooldown=5,
            image_path="Card/CardIcon/shield_broken.png"
        )

    def use_card(self, battle):
        damage = battle.mob.shield
        battle.mob.shield = 0
        card_effect.deal_damage(damage,battle)

class MistVeil(CardSetting):
    def __init__(self):
        super().__init__(
            name="Mist Veil",
            mana_cost=2,
            description="Apply 3 stack of Mist and 1 stack of Lost effect to enemy.",
            card_type="Effect",
            rarity="Rare",
            cooldown=6
        )

    def use_card(self, battle):
        battle.mob.add_effect(Mist(3))
        battle.mob.add_effect(Lost())

class DeepMist(CardSetting):
    def __init__(self):
        super().__init__(
            name="Deep Mist",
            mana_cost=1,
            description="Apply 6 stack of Mist effect to enemy.\nAt the end of your next turn, set the enemy's Mist stacks to 3 ",
            card_type="Effect",
            rarity="Rare",
            cooldown=3
        )

    def use_card(self, battle):
        battle.mob.add_effect(Mist(6))
        for effect in battle.mob.get_effects():
            if effect.name == "Mist":
                effect.activate_fixed_duration = True
                effect.fixed_duration = 2
        
class MidnightHour(CardSetting):
    def __init__(self):
        super().__init__(
            name="Midnight Hour",
            mana_cost=1,
            description="Apply Midnight effect to enemy, last fot 2 rounds.\nMidnight: Mist damage cannot be blocked by shields\nthe same amount of damage is then dealt to the shield.",
            card_type="Effect",
            rarity="Rare",
            cooldown=4
        )

    def use_card(self, battle):
        battle.mob.add_effect(Midnight())
        
class MistHunt(CardSetting):
    def __init__(self):
        super().__init__(
            name="Mist Hunt",
            mana_cost=2,
            description="Deal 1 damage. Reduce the stack of Mist effect on enemy by 1,\nthen deal damage equals to the stack of Mist effect.",
            card_type="Attack",
            rarity="Rare",
            cooldown=4
            
        )
        self.additional_attack = False

    def use_card(self, battle):
        print("Mist Hunt used")
        card_effect.deal_damage(1, battle)
        self.additional_attack = True
    
    def additional_action(self, battle):
        print("Mist Hunt additional action activated")
        for effect in battle.mob.get_effects():
            if effect.name == "Mist":
                effect.stack -=1
                if effect.stack >0 :
                    effect.activate(battle)

class MistBlade(CardSetting):
    def __init__(self):
        super().__init__(
            name="Mist Blade",
            mana_cost=1,
            description="Deal 1 damage. Clear all Mist stacks on enemy, then increase this card's additional attack by the number of Mist stacks cleared.",
            card_type="Attack",
            rarity="Rare",
            cooldown=3
        )
        self.additional_damage = 0
        self.activated_times = 0
    def use_card(self, battle):
        card_effect.deal_damage(1 + self.additional_damage, battle)
        if self.additional_damage > 0:
            self.activated_times +=1
            if self.activated_times >=2:
                self.additional_damage =0
                self.mana_cost -=1
        for effect in battle.mob.get_effects():
            if effect.name == "Mist":
                self.additional_damage += effect.stack
                self.mana_cost +=0
                battle.mob.remove_effect(effect)
                break

class ShadowOfTheMist(CardSetting):
    def __init__(self):
        super().__init__(
            name = "Shadow of the Mist",
            mana_cost=0,
            description="When dealing damage to enemy using attack cards, add 1 stack of Midnight effect to enemy, last for 2 rounds.",
            card_type="Passive",
            rarity="Rare",
            cooldown=0
            )
        self.activate_on_attack = True
    def use_card(self, battle):
        pass
    def activate_effect(self, battle):
        battle.mob.add_effect(Midnight())

class RuinedForge(CardSetting):
    def __init__(self):
        super().__init__(
            name = "Ruined Forge",
            mana_cost=0,
            description="Inflict 2 stacks of Mist when you use cards other than attack cards.\nMist: At the start of enemy's turn, deal 1 damage per Mist stack.",
            card_type="Passive",
            rarity="Rare",
            cooldown=0
            )
        self.activate_on_attack = False
    def use_card(self, battle):
        pass
    def activate_effect(self, battle):
        battle.mob.add_effect(Mist(2))

class CandyBullet(CardSetting):
    def __init__(self):
        super().__init__(
            name="Candy Bullet",
            mana_cost=2,
            description="Deal 4 damage. Apply effect Candy to the target.\nCandy: When enemy holding this effect, attack enemy will randomly reduce two card's cooldown by 1.",
            card_type="Attack",
            rarity="Rare",
            cooldown=5
        )

    def use_card(self, battle):
        card_effect.deal_damage(4, battle)
        battle.mob.add_effect(Candy())

class SweetSolace(CardSetting):
    def __init__(self):
        super().__init__(
            name="Sweet Solace",
            mana_cost=2,
            description="Reduce all the card's maximum cooldown by 1.",
            card_type="Effect",
            rarity="Rare",
            cooldown=6
        )
        self.effect_on_card = True
        self.effect_on_battle_content = False

    def use_card(self, deck):
        for card in deck.current_deck:
            if card.cooldown > 0:
                card.cooldown -= 1
                # for card in deck.current_deck:
                #     print(f"Card: {card.name}, Cooldown: {card.current_cooldown}")

class OathOfResolve(CardSetting):
    def __init__(self):
        super().__init__(
            name="Oath of Resolve",
            mana_cost=2,
            description="When the game starts, increase all cards maximum cooldown by 3. Reduce the damage dealt of this card by the sum of all cards' maximum cooldowns. Deal 60 damage to enemy.",
            card_type="Attack",
            rarity="Rare",
            cooldown=7
        )
        self.effect_on_card = True
        self.effect_on_battle_content = True
        self.activate_on_game_start = True


    def use_card(self, battle,deck):
        basic_damage = 60
        reduction = 0
        for card in deck.current_deck:
            print(f"{card.name}: {card.cooldown}")
            reduction += card.cooldown
        final_damage = basic_damage - reduction
        print(f"value of final damage: {final_damage}")
        card_effect.deal_damage(final_damage, battle)

    def activate_effect(self,deck):
        for card in deck.current_deck:
            card.cooldown +=3
class Redemption(CardSetting):
    def __init__(self):
        super().__init__(
            name="Redemption",
            mana_cost=2,
            description="End the cooldown of the card that have the highest cooldown. According to the cooldown remain, increase the cooldown of this card for 1 time. Restore mana to full.",
            card_type="Effect",
            rarity="Rare",
            cooldown=16
        )
        self.effect_on_card = True
        self.effect_on_battle_content = True
    
    def use_card(self, battle,deck):
        max = 0
        target_card = None
        for card in deck.current_deck:
            if card.current_cooldown >max:
                max = card.current_cooldown
                target_card = card
        if not target_card:
            return
        else:
            target_card.current_cooldown = 0
            battle.player.mana = battle.player.max_mana

class Card_list():
    def __init__(self):
        self.card_list = [NormalAttack(),Heal(),Defense(),ShieldCounter(),
                          HolyLight(),Intimidate(),CriticalStrike(),Trick(),CandyBomb(),MistVeil(),
                          DeepMist(),MidnightHour(),MistHunt(),MistBlade(),ShadowOfTheMist(),
                          RuinedForge(),CandyBullet(),SweetSolace(),OathOfResolve(), Redemption()
                          ]
    
    # def save_cards_to_json(self, filename="Data/CardDetails.json"):
    #     """
    #     Store all card details in a JSON file
    #     """
    #     import json
    #     # from inspect import getsource
        
    #     card_data = {"cards": []}
        
    #     for card in self.card_list:
    #         # Get the class definition to analyze use_card method
    #         # class_source = getsource(card.__class__)
            
    #         # # Extract the actions from use_card method
    #         # actions = []
    #         # if "deal_damage" in class_source:
    #         #     value = int(''.join(filter(str.isdigit, 
    #         #         [line for line in class_source.split('\n') if "deal_damage" in line][0])))
    #         #     actions.append({"action": "deal_damage", "value": value})
    #         # if "heal" in class_source:
    #         #     value = int(''.join(filter(str.isdigit, 
    #         #         [line for line in class_source.split('\n') if "heal" in line][0])))
    #         #     actions.append({"action": "heal", "value": value})
    #         # if "shield" in class_source:
    #         #     value = int(''.join(filter(str.isdigit, 
    #         #         [line for line in class_source.split('\n') if "shield" in line][0])))
    #         #     actions.append({"action": "shield", "value": value})
    #         # if "add_effect" in class_source:
    #         #     effect_name = class_source.split("add_effect(")[1].split(")")[0]
    #         #     actions.append({"action": "add_effect", "effect": effect_name})
            
    #         card_details = {
    #             "name": card.name,
    #             "mana_cost": card.mana_cost,
    #             "description": card.description,
    #             "type": card.type,
    #             "rarity": card.rarity,
    #             "cooldown": card.cooldown,
    #             "image_path": card.image_path,
    #             "background_story": card.background_story,
    #             # "use_card": {"actions": actions} if len(actions) > 1 else actions[0] if actions else {}
    #         }
            
    #         card_data["cards"].append(card_details)
        
    #     # Write to JSON file with proper formatting and UTF-8 encoding
    #     with open(filename, 'w', encoding='utf-8') as f:
    #         json.dump(card_data, f, ensure_ascii=False, indent=4)

class CandyBomb(CardSetting):
    def __init__(self):
        super().__init__(
            "Candy Bomb",
            2,
            "Deal 3 damage. Apply effect Candy to the target.\nCandy: Every time when enemy's health is reduced by your attack, reduce one of your card's cooldown, lasts 3 turns.",
            "Attack",
            "Rare",
            3
        )

    def use_card(self, battle):
        effect = CardEffect()
        effect.deal_damage(3, battle)
        battle.mob.add_effect(effect.Candy())
