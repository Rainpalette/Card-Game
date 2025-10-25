class Effect:
    def __init__(self, name, description, duration, effect_type, stack):
        self.name = name
        self.description = description
        self.duration = duration
        self.activated_times = 0
        self.types = ["WhenHolding", "OnTurnStart", "OnTurnEnd", "OnAttack", "OnDamaged", "Passive"]
        self.type = effect_type  # e.g., "WhenHolding", "OnTurnStart", etc.
        self.stack = stack
        self.duration_by_stack = False