from Card.Effect import Effect
import random
class CardEffect:
    def __init__(self):
        self.card = None
        self.mob = None
        self.player = None

    def deal_damage(self, damage, battle):
        damage_dealt = battle.mob.shield - (damage + battle.player.attack - battle.mob.defense)
        if damage_dealt < 0:
            battle.mob.health += damage_dealt
            battle.mob.shield = 0
        else:
            battle.mob.shield -= damage + battle.player.attack - battle.mob.defense

    def deal_damage_to_player(self, damage, battle):
        damage_dealt = battle.player.shield - (damage + battle.mob.attack - battle.player.defense)
        if damage_dealt < 0:
            battle.player.health += damage_dealt
            battle.player.shield = 0
        else:
            battle.player.shield -= damage + battle.mob.attack - battle.player.defense

    def deal_damage_ignore_shield(self, damage, battle):
        battle.mob.health -= damage + battle.player.attack - battle.mob.defense

    def deal_damage_to_player_ignore_shield(self, damage, battle):
        battle.player.health -= damage + battle.mob.attack - battle.player.defense

    def heal(self, heal, battle):
        battle.player.health += heal
        if battle.player.health > battle.player.max_health:
            battle.player.health = battle.player.max_health

    def shield(self, shield, battle):
        battle.player.shield += shield

    def reduce_cooldown(self, reduce):
        self.card.cooldown -= reduce

    def increase_cooldown(self, increase):
        self.card.cooldown += increase

    def apply_effect(self, effect, stack):
        effect_methods = {
            "Fog": self.Fog,
            "Icy": self.Icy,
            "Memory": self.Memory,
            "WinterFestival": self.WinterFestival,
            "IronBlooded": self.IronBlooded,
            "Lost": self.Lost,
            "Midnight": self.Midnight,
            "Candy": self.Candy,
            "Tourniquet": self.Tourniquet,
            "PaletteCorrosion": self.PaletteCorrosion,
            "Void": self.Void
        }
        if effect.name in effect_methods:
            return effect_methods[effect.name](stack)
        else:
            print("Unknown effect")

    def Fog(self, stack):
        description = "Damage over time. Reduce health at the end of turn by the number of stack of this effect."
        current_effect = Effect("Fog", description, 3, "OnTurnEnd", stack)
        current_effect.DurationByStack = True
        return current_effect

    def Icy(self):
        description = "Cannot use any card. At the end of turn, choose a card and reduce the cooldown of the card by 2."
        current_effect = Effect("Icy", description, 2, "OnTurnEnd", 1)
        return current_effect

    def Memory(self,battle):
        description = "Reduce attack by 1, reduce defense by 1."
        current_effect = Effect("Memory", description, 3, "WhenHolding", 1)
        battle.mob.defense -=1
        return current_effect

    def WinterFestival(self):
        description = "At the end of turn, heal 5 health. Lasts for 3 turns."
        current_effect = Effect("WinterFestival", description, 3, "WhenHolding", 1)
        return current_effect

    def IronBlooded(self):
        description = "At the start of turn, gain 5 shield. Lasts for 3 turns."
        current_effect = Effect("IronBlooded", description, 3, "WhenHolding", 1)
        return current_effect

    def Lost(self):
        description = "At the start of turn, lose 5 health. Lasts for 3 turns."
        current_effect = Effect("Lost", description, 3, "OnDamaged", 1)
        return current_effect

    def Midnight(self):
        description = "At the start of turn, gain 5 mana. Lasts for 3 turns."
        current_effect = Effect("Midnight", description, 3, "WhenHolding", 1)
        return current_effect

    def Candy(self):
        description = "At the end of turn, gain 5 mana. Lasts for 3 turns."
        current_effect = Effect("Candy", description, 3, "OnDamaged", 1)
        return current_effect

    def Tourniquet(self, stack):
        description = "At the end of turn, lose 5 health. Lasts for 3 turns."
        current_effect = Effect("Tourniquet", description, 3, "OnTurnEnd", stack)
        current_effect.DurationByStack = True
        return current_effect

    def PaletteCorrosion(self, stack):
        description = "At the start of turn, reduce 1 mana. Lasts for 3 turns."
        current_effect = Effect("PaletteCorrosion", description, 3, "OnTurnEnd", stack)
        current_effect.DurationByStack = True
        return current_effect

    def Void(self, stack):
        description = "No effect. Considered as a negative effect."
        current_effect = Effect("Void", description, 0, "WhenHolding", stack)
        current_effect.DurationByStack = True
        return current_effect


# def Memory(self,battle):
#         description = "Reduce attack by 1, reduce defense by 1."
#         current_effect = Effect("Memory", description, 3, "WhenHolding", 1)
#         battle.mob.defense -=1
#         return current_effect


#create a template for all effects to inherit
class EffectTemplate():
    def __init__(self):
        self.name = ""
        self.description = ""
        self.duration = 0
        self.activated_times = 0
        # self.types = ["WhenHolding", "OnTurnStart", "OnTurnEnd", "OnAttack", "OnDamaged", "Passive"]
        self.type = ""
        self.stack = 0
        self.DurationByStack = False
        self.image_path = "GUI/BattlePage/D.D.jpg"
        self.stackable = True
        self.effect_on_card = False
        # self.current_duration = self.duration
    def apply_effect(self, battle):
        pass

    def remove_effect(self,battle=""):
        pass
class defenseReduction(EffectTemplate):
    def __init__(self):
        super().__init__()
        self.name = "defenseReduction"
        self.description = "Reduce defense by 1."
        self.dedault_duration = 3
        self.duration = 3
        self.activated_times = 0
        self.types = ["WhenHolding", "OnTurnStart", "OnTurnEnd", "OnAttack", "OnDamaged", "Passive"]
        self.type = "WhenHolding"
        self.stack = 1
        self.DurationByStack = False
        self.image_path = "GUI/BattlePage/D.D.jpg"
        # self.current_duration = self.duration
    def apply_effect(self, battle):
        battle.mob.defense -= 1
        self.activated_times += 1

    def remove_effect(self, battle):
        battle.mob.defense += 1

class Mist(EffectTemplate):
    def __init__(self, stack):
        super().__init__()
        self.name = "Mist"
        self.description = "Deal damage equals to the stack of this effect at the end of turn."
        self.duration = stack
        self.defaultduration = stack
        self.activated_times = 0
        self.types = ["WhenHolding", "OnTurnStart", "OnTurnEnd", "OnAttack", "OnDamaged", "Passive"]
        self.type = "OnTurnEnd"
        self.effect_type = "DamageOverTime"
        self.stack = stack
        self.DurationByStack = True
        self.image_path = "GUI/BattlePage/D.D.jpg"
        self.fixed_duration = 2
        self.activate_midnight = False
        self.activate_fixed_duration = False
        self.card_effect = CardEffect()
        # self.current_duration = self.duration
    def apply_effect(self, battle):
        print("Applying Mist effect with stack:", self.stack)
        for effect in battle.mob.get_effects():
            
            if effect.name == "Midnight":
                # self.card_effect.deal_damage_ignore_shield(self.stack, battle)
                # self.activated_times += 1
                self.apply_midnight(battle)
                return
        self.card_effect.deal_damage(self.stack, battle)
        self.activated_times += 1

    def remove_effect(self,battle=""):
        pass
    
    def turn_down_mist(self):
        self.stack = 3
    
    def apply_midnight(self, battle):
        self.card_effect.deal_damage_ignore_shield(self.stack, battle)
        if battle.mob.shield > 0 and battle.mob.shield <= self.stack:
            battle.mob.shield = 0
        elif battle.mob.shield > self.stack:
            battle.mob.shield -= self.stack
    
    def activate(self, battle):
        for effect in battle.mob.get_effects():
            if effect.name == "Midnight" and self.stack > 0:
                self.apply_midnight(battle)
                return
        if self.stack >0:
            self.apply_effect(battle)


class Lost(EffectTemplate):
    def __init__(self):
        super().__init__()
        self.name = "Lost"
        self.description = "Gain equal stack of effect 'Mist' as the damage taken.\nLost this effect after taking one incoming damage."
        self.duration = 99
        self.default_duration = 99
        self.activated_times = 0
        self.types = ["WhenHolding", "OnTurnStart", "OnTurnEnd", "OnAttack", "OnDamaged", "Passive"]
        self.type = "OnDamaged"
        self.stack = 1
        self.DurationByStack = False
        self.image_path = "GUI/BattlePage/D.D.jpg"
        # self.current_duration = self.duration
    def apply_effect(self, battle, damage_taken):
        for effect in battle.mob.get_effects():
            if effect.name == "Mist":
                effect.stack += damage_taken
                for effect in battle.mob.get_effects():
                    if effect.name == "Lost":
                        battle.mob.remove_effect(effect)
                        print("Lost effect removed after triggering.")
                        return
        new_effect = Mist(damage_taken)
        battle.mob.add_effect(new_effect)
        self.activated_times += 1
        for effect in battle.mob.get_effects():
            if effect.name == "Lost":
                battle.mob.remove_effect(effect)
                print("Lost effect removed after triggering.")


    def remove_effect(self,battle=""):
        pass

class Midnight(EffectTemplate):
    def __init__(self):
        super().__init__()
        self.name = "Midnight"
        self.description = "Mist damage cannot be blocked by shields\nthe same amount of damage is then dealt to the shield."
        self.duration = 2
        self.activated_times = 0
        self.types = ["WhenHolding", "OnTurnStart", "OnTurnEnd", "OnAttack", "OnDamaged", "Passive"]
        self.type = "WhenHolding"
        self.stack = 1
        self.DurationByStack = False
        self.image_path = "GUI/BattlePage/D.D.jpg"
        # self.current_duration = self.duration
    def apply_effect(self, battle):
        for effect in battle.mob.get_effects():
            if effect.name == "Mist":
                effect.activate_midnight = True
        self.activated_times += 1

    def remove_effect(self,battle=""):
        for effect in battle.mob.get_effects():
            if effect.name == "Mist":
                effect.activate_midnight = False

class Candy(EffectTemplate):
    def __init__(self):
        super().__init__()
        self.name = "Candy"
        self.description = "When enemy holding this effect, attack enemy will randomly reduce two card's cooldown by 1."
        self.duration = 3
        self.activated_times = 0
        self.types = ["WhenHolding", "OnTurnStart", "OnTurnEnd", "OnAttack", "OnDamaged", "Passive"]
        self.type = "OnAttack"
        self.stack = 1
        self.DurationByStack = False
        self.image_path = "GUI/BattlePage/D.D.jpg"
        self.effect_on_card = True
        # self.current_duration = self.duration
    def apply_effect(self, deck):
        print("Applying Candy effect to reduce cooldowns.")
        cards_on_cooldown = [card for card in deck.current_deck if card.current_cooldown > 0]
        if len(cards_on_cooldown) == 0:
            return
            
        # Determine how many cards to reduce cooldown for (up to 2, but limited by available cards)
        num_cards = min(2, len(cards_on_cooldown))
        random_indices = random.sample(range(len(cards_on_cooldown)), num_cards)
        
        for i in random_indices:
            card = cards_on_cooldown[i]
            if card.current_cooldown > 0:
                card.current_cooldown -= 1
                print("Current cooldown of card", card.name, "reduced to", card.current_cooldown)
                self.activated_times += 1
            
            

    def remove_effect(self,battle=""):
        pass