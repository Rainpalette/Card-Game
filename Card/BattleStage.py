from enum import Enum
from Card.PlayerSetting import *
from Card.MobSetting import *
from Card.CardEffect import *
from Card.GameSetting import *
from Card.DeckStage import *
from Card.BattleContent import *
from Card.CardSetting import *


class usableMob(MobSetting):
    def __init__(self):
        super().__init__()
    
    def use_skill(self):
        return super().use_skill()

class BattleStage:
    class Boss(Enum):
        Radiel = 1
        Jonathan = 2

    def __init__(self):
        self.mob = usableMob()
        self.player = PlayerSetting("Hero", 50, 2, 0)
        self.player_copy = self.player
        self.card_effect = CardEffect()
        # self.card_setting = CardSetting(card_effect=self.card_effect)
        self.game = GameSetting()
        self.player_deck = DeckStage()
        self.battle = BattleContent(self.mob, self.player)
        self.card_deck=None
        self.on_event = None
    
    def trigger_event(self, event_type, data=None):
        if self.on_event:
            self.on_event(event_type, data)

    def start_battle(self, boss):
        if boss == self.Boss.Radiel:
            self.mob = usableMob("Radiel", 50, 2)
        elif boss == self.Boss.Jonathan:
            self.mob = usableMob("Jonathan", 80, 2)
        elif boss == "crown":
            self.mob = crown(self.battle)
            print("mob is crown")
        self.battle = BattleContent(self.mob, self.player)
        self.mob.battle = self.battle
        self.mob.setup()
        self.player.reset()
        self.card_deck = PlayerCardManager(self.battle,self.player_deck)

    def get_battle(self):
        return self.battle

    def get_player_deck(self):
        return self.player_deck

    def get_mob(self):
        return self.mob

    def get_player(self):
        return self.player

    def is_battle_over(self):
        if self.battle.player.health <= 0 or self.battle.mob.health <= 0:
            return True
        return False

    def is_player_win(self):
        return self.mob.health <= 0

    def end_turn(self, deck_stage):
        for card in deck_stage:
            if card.current_cooldown > 0:
                card.current_cooldown -= 1

        for effect in self.player.get_effects():
            if effect.type == "OnTurnEnd":
                print("Applying player end turn effect:", effect.name)
                effect.apply_effect(self.battle)
                if effect.DurationByStack:
                    effect.stack -= 1
                    print(f"Effect {effect.name} stack decreased to {effect.stack}")
                    # effect.duration = effect.stack
                    if effect.stack <= 0:
                        self.player.remove_effect(effect)
                        continue
            effect.duration -= 1
            if effect.duration <= 0:
                self.player.remove_effect(effect)
                effect.remove_effect(self.battle)

        for effect in self.mob.get_effects():
            if effect.type == "OnTurnEnd":
                effect.apply_effect(self.battle)
                if effect.DurationByStack:
                    effect.stack -= 1
                    # effect.duration = effect.stack
                    if effect.stack <= 0:
                        self.mob.remove_effect(effect)
                        continue
            effect.duration -= 1
            if effect.duration <= 0:
                self.mob.remove_effect(effect)
                effect.remove_effect(self.battle)
            #Special handling for Mist effect
            if effect.name == "Mist" and effect.activate_fixed_duration:
                effect.fixed_duration -= 1
                if effect.fixed_duration <= 0:
                    effect.turn_down_mist()
                    effect.activate_fixed_duration = False
            # if effect.name == "Mist" and (effect.activate_midnight):
            #     effect.apply_midnight(self.battle)
            #     effect.activate_midnight = False


    def start_turn(self):
        self.player.mana = self.player.max_mana
        self.mob.mana = self.mob.max_mana
        self.game.turn += 1

        for effect in self.player.get_effects():
            if effect.type == "OnTurnStart":
                self.card_effect.apply_effect(effect, effect.stack)

        for effect in self.mob.get_effects():
            if effect.type == "OnTurnStart":
                self.card_effect.apply_effect(effect, effect.stack)

    def boss_turn(self):
        skill_name = self.mob.use_skill()
        return skill_name
        # while True:
        #     if self.mob.mana <=0:
        #         return
        #     if self.is_battle_over():
        #         return
        #     self.mob.use_skill()

    # def player_turn(self):
    #     print("player")

    def check_card_mana(self, card):
        return card.mana_cost <= self.battle.player.mana

    def check_card_cooldown(self, card):
        return card.current_cooldown < 0

    def play_card(self, card, additional_attack=False):
        if additional_attack:
            card.additional_action(self.battle)
            return
        card.use_card(self.battle)
        self.player.mana -= card.mana_cost
        
        card.cooldown_card()
        

    def calculate_damage(self, healthBefore, healthAfter):
        base_damage = healthBefore - healthAfter
        return base_damage