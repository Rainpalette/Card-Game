from Card.Effect import Effect
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

class defenseReduction():
    def __init__(self):
        self.name = "defenseReduction"
        self.description = "Reduce defense by 1."
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
