XP_BASE = 10  # Base XP multiplier

# Cossack ranks: (minimum level, title)
RANKS = [
    (1, "Джура"),
    (3, "Козак"),
    (5, "Десятник"),
    (8, "Хорунжий"),
    (12, "Осавул"),
    (17, "Сотник"),
    (23, "Полковник"),
    (30, "Гетьман"),
]


class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.exp = 0
        self.level = 1
        self.last_daily = None  # ISO date of the last /daily, Kyiv time
        self.streak = 0

    @property
    def title(self):
        return [name for min_level, name in RANKS if self.level >= min_level][-1]

    @property
    def total_xp(self):
        """All XP ever earned: the cost of every passed level plus current XP."""
        return XP_BASE * self.level * (self.level - 1) // 2 + self.exp

    def exp_handler(self, amount: int):
        """Add (or subtract) XP and update level accordingly."""
        start_level = self.level
        self.exp += amount

        # XP loss can drop several levels at once (e.g. a lost duel)
        while self.exp < 0 and self.level > 1:
            self.level -= 1
            self.exp += self.level * XP_BASE

        # Clamp XP to 0 at level 1
        if self.exp < 0:
            self.exp = 0

        while self.exp >= self.level * XP_BASE:
            self.exp -= self.level * XP_BASE
            self.level += 1

        if self.level > start_level:
            return "level_up"
        if self.level < start_level:
            return "level_down"
        return "none"
