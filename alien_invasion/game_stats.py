class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start Alien Invasion in an active state.
        self.game_active = False
        # When you want to add AI to this game, just change this value to True
        # instead of False.
        # High score should never be reset. which is why it is here and not
        # in reset_stats.
        self.high_score = 0
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

# Interesting, so we can use a class's own methods in its own definition even
# though the method was only defined afterwards.
# We intialize the score in reset_stats() to ensure that the score goes back to
# 0 whenever the game restarts

# You should've recognized the new strategy that Matthes uses with
# __init__ methods. If he wants an __init__ attribute to change over time
# he puts the attribute in another method in the class and just calls
# the method in the __init__ method