import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Make a ship
    ship = Ship(ai_settings, screen)
    # Make a group to store bullets in.
    bullets = Group()
    aliens = Group()
    # Make a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
            aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, 
                              bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, 
                             bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)

run_game()

# So let's break it down. This code is the basic structure of a game written
# in Pygame. The pygame module contains the functionality needed to make a
# game. We'll use the sys module to exit the game when the player quits.
# Alien Invasion starts as the function run_game(). The line pygame.init()
# initializes background settings that Pygame needs to work properly.

# We call pygame.display.set_mode() to create a display window called screen
# on which we'll draw all of the game's graphical elements. The argument
# (1200, 800) is a tuple that defines the dimensions of the game window.
# This action creates a game window 1200 pixels wide and 800 pixels high.

# The screen object is called a surface. A surface in Pygame is a part of the
# screen where you display a game element. Each element in the game, like the
# aliens or the ship, is a surface. The surface returned by display.set_mode()
# represents the entire game window. When we activate the game's animation
# loop, this surface is automatically redrawn on every pass through the loop.

# The game is controlled by a while loop that contains an event loop and code
# that manages screen updates. An event is an action that the user performs
# while playing the game, such as pressing a key or moving the mouse.
# To make our program respond to events, we'll write an event loop to listen
# for an event and perform an appropriate task depending on the kind of 
# event that occurred. The for loop in the code is an event loop.

# To access the events detected by Pygame, we'll use the pygame.event.get()
# method. Any keyboard or mouse event will cause the for loop to run.
# Inside the loop, we'll write a series of if statements to detect and respond
# to specific events. For example, when the player clicks the game window's
# close button, a pygame.QUIT event is detected and we call sys.exit() to
# exit the game.

# The previous paragraph now has its code in game_functions.py as check_events

# The call to pygame.display.flip() tells Pygame to make the most recently
# drawn screen visible. In this case (first edition of code) it draws an 
# empty screen each time through the while loop to erase the old screen so that
# only the new screen is visible. When we move the game elements around,
# pygame.display.flip() will continually update the display to show the new
# positions of elements and hide the old ones, creating the illusion of smooth
# movement.

# The last line in this basic game structure calls run_game(), which initializes
# the game and starts the main loop.

# With bg_color and the fill method, we filled the screen with light gray.
# The fill method takes a 3-element tuple of rgb values

# We then import Ship (class) and then make an instance of Ship (named ship)
# after the screen has been created. It must come before the main while loop so
# we don't make a new instance of the ship on each pass through the loop.
# We draw the ship onscreen by calling ship.blitme() after filling the back-
# ground, so the ship appears on top of the background

# The new update_screen() function comes from the module game_functions. It
# takes three parameters: ai_settings (an instance of the Settings class),
# screen (the created window display for the game), and ship (an instance
# of the Ships class).

# We are trying to write code that fires a bullet each time the player presses
# the spacebar. First, we'll create a group in alien_invasion to store all the
# live bullets so we can manage the bullets that have already been fired. This
# group will be an instance of the class pygame.sprite.Group which behaves like
# a list with some extra functionality.

# We'll use this group to draw bullets to the screen on each pass through the
# main loop and to update each bullet's position. The instance of Group will
# be called bullets. We pass bullets to check_events() and update_screen()
# so the bullets can interact with key presses and change its location on the
# screen.

# When you call update() on a group, the group automatically calls update() for
# each sprite in the group. The line bullets.update() calls bullet.update() for
# each bullet we place in the group bullets.

# In the while True loop, there is a line that says bullets.update(). This line
# calls the update method for every bullet in the bullets list, and since
# every bullet is an instance of the Bullet class. The update tells it to move
# continuously upwards. Unlike ship, there is no moving flag to stop them.
# The update method just keeps moving the bullet based on the speed factor. It's
# indefinite.

# So now we gotta remove bullets that have gotten out of the screen. To do this,
# we're gonna need to loop through a copy of the bullets list. The reason is
# because we don't want to remove items from a list or group within a for loop.
# To accomplish this task, we use the copy method and a conditional to remove
# the escaping bullets. We iterate over a copy of the list to ensure safety
# success of code, but we still remove elements from the actual bullets list.