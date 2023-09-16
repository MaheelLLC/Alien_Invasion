import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Making the ship object"""
# We changed ship to be a sprite so we can add more of them to the screen
# like the ship lives.
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flags."""
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # If we used elif here, moving_right will always have priority

        # Update rect object from self.center.
        self.rect.centerx = self.center
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
# Let's break down all of this nonsense. Note: The blit() method draws 
# the image.
# First, we import the pygame module as usual. The __init__() method of Ship
# takes two parameters: the self reference and the screen where we'll draw
# the ship. To load the image, we call pygame.image.load(). This function
# returns a surface representing the ship, which we store in self.image

# Once the image is loaded, we use get_rect() to access the surface's rect
# attribute. One reason Pygame is so efficient is that it lets you treat game
# elements like rectangles (rects), even if they're not exactly shaped as one

# When working with a rect object, you can use the x- and y-coordinates of the
# top, bottom, left, and right edges of the rectangle, as well as the center
# You can set any of these values to determine the current position of the rect.

# When you're centering a game element, work with the center, centerx, or
# centery attributes of a rect. When you're working at an edge of the screen,
# work with the top, bottom, left, or right attributes. When you're adjusting
# the horizontal or vertical placement of the rect, you can just use the x and
# y attributes, which are the x- and y-coordinates of its top-left corner.

# In Pygame, the origin(0,0) is at the top-left corner of the screen, and 
# coordinates increase as you go down and to the right. On a 1200 by 800 screen
# the bottomr-right corner has the coordinates (1200, 800)

# By the way, the image's measurements comes from the actual image's bitmap
# canvas measurements. If you open the image in an image editor, you'll 
# actually see that the ship is 60 by 48 pixels

# We'll position the ship at the bottom center of the screen. To do so, first
# store the screen's rect in self.screen_rect (we're making a measured canvas
# here), and then make the value of self.rect.centerx (the x-coordinate of
# the ship's center) match the centerx attribute of the screen's rect. Make
# the value of self.rect.bottom (the y-coordinate of the ship's bottom) equal
# to the value of the screen rect's bottom attribute. Pygame will use these
# rect attributes to position the ship image so it's centered horizontally
# and aligned with the bottom of the screen.

# We also define the blitme() method, which will draw the image to the screen
# at the position specified by self.rect. The self.screen.blit is saying
# draw something on the screen. The parameters of the blit() method will
# tell Python what to draw on the screen. The parameters specifically are the
# image itself and its rectangular surface (AKA its hitbox ;) )

# On game_functions, we managed to let Python recognize the right arrow key
# as a right movement key...But it has to be clicked multiple times for the
# ship to actually look like it's moving. Thus, to make the ship continuously
# move right when a player holds the right key and stop when the player
# releases it, we gotta have a pygame.KEYUP event so we'll know when they
# released the key

# So we'll use the KEYDOWN and KEYUP events together with a flag called
# moving_right to implement continuous motion

# When the ship is motionless, the moving_right will be False. When the 
# right arrow key is pressed, we'll set the flag to True, and when it's
# released, we'll set the flag to False again.

# Thus, we're gonna give the Ship class controls all attributes of the ship,
# so we'll give it an attribute called moving_right and an update() method will
# change the position of the ship if the flag is set to True. We'll call this
# method any time we want to update the position of the ship.

# Update will only work when the moving_right flag is true.

# This time, we choose the speed of the ship based on the speed factor
# attribute that we made in the Settings class
# We access this attribute by creating an __ini__ parameter called ai_settings
# ai_settings happens to be the same name as the instance for Settings class
# in our alien_invasion python file.

# Now, that we can access the speed factor. We just create a new attribute
# called self.center which is just the float/decimal value of the
# horizontal center of the ship's rectangular surface (rect.centerx).
# Then we add or subtract the speed factor to this new attribute in the
# conditional of the moving_right or moving_left flags respectively.
# Finally, we set the rect.centerx to self.center to update to the new
# center value of the ship since rect.centerx controls the center of the ship.
# Do realize that only the integer portion of self.center will be stored in
# rect.centerx.

# Now to keep the ship within the bounds of the screen, we need to make sure
# that its horizontal position isn't beyond the edges of the screen. We can
# access the edges of the ship's rectangular surface with rect.right and 
# rect.left. Now, we just make sure rect.right isn't greater than the screen's
# right edge's x position and rect.left isn't less than 0 (since the left edge
# of the screen is on the origin axis).