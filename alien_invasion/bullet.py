import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A (subclass/child) class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

# So Bullet is a sub class of the Sprite class from pygame. To create the
# bullet, the init method needs the ai_settings, screen, and ship instances
# and we call super() to properly inherit from Sprite

# As usual we need to make a rectangular surface for the bullet object.
# However, the bullet is not an actual image, so we gotta make the rect from
# scratch which is what the Rect class does.

# Afterwards, we gotta place the bullet in horizontal center of the ship and
# then, on the ship's top which is what centerx and top does

# Since the bullet is only moving vertically, we're gonna convert its vertical
# position to a float and store it in the variable self.y.

# Also, since we put all of the bullet settings in the Settings class. We can
# store the color and speed factor of the bullet from ai_settings instance to
# the attributes color and speed_color

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

# Now we have two methods. One "updates" the bullet's y position upwards. The
# other draws the actual bullet with the arguments screen, color, and rect
# surface.

# The draw.rect() function fills the part of the screen defined by the bulley's
# rect with the color stored in self.color
