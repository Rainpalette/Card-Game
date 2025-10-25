from abc import ABC, abstractmethod
from Card.CardEffect import *


card_effect = CardEffect()
class CardSetting(ABC):
    def __init__(self, name="", mana_cost=0, description="", card_type="", rarity="", cooldown=0):
        self.name = name
        self.mana_cost = mana_cost
        self.description = description
        self.type = card_type
        self.rarity = rarity
        self.cooldown = cooldown
        self.current_cooldown = 0

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
            cooldown=3
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
            cooldown=2
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
            cooldown=2
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
        battle.mob.add_effect(card_effect.Memory(battle))


class CriticalStrike(CardSetting):
    def __init__(self):
        super().__init__(
            name="Critical Strike",
            mana_cost=1,
            description="Deal 8 damage to the enemy.",
            card_type="Attack",
            rarity="Common",
            cooldown=5
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
            cooldown=5
        )

    def use_card(self, battle):
        damage = battle.mob.shield
        battle.mob.shield = 0
        card_effect.deal_damage(damage,battle)

class Card_list():
    def __init__(self):
        self.card_list = [NormalAttack(),Heal(),Defense(),ShieldCounter(),
                          HolyLight(),Intimidate(),CriticalStrike(),Trick(),CandyBomb()]

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
