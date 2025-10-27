class PlayerSetting:
    def __init__(self, name="", health=0, mana=0, shield=0):
        self.name = name
        self.health = health
        self.before_change_health = health
        self.mana = mana
        self.effects = []
        self.shield = shield
        self.shield_before_change = 0
        self.max_mana = 2
        self.maximal_mana = 6
        self.defense = 0
        self.attack = 0
        self.max_health = health

    def add_effect(self, effect):
        self.effects.append(effect)

    def add_multiple_effect(self, effect, stack):
        effect.stack = stack
        self.effects.append(effect)

    def remove_effect(self, effect):
        if effect in self.effects:
            self.effects.remove(effect)

    def get_effects(self):
        return self.effects
    
    def reset(self):
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = 0
        self.attack = 0
        self.defense = 0
        self.effects =[]

    # def apply_effect(self, effect):
    #     # Implement effect application logic here
    #     if effect.name == "Heal":
    #         self.health += 10  # Example: Heal for 10 health points
    #     # Add more effect types as needed