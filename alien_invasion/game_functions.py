import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, 
                         bullets):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)

# Note: Naming parameters as the same thing as your arguments helps ALOT with
# keeping your code consistent and correct.

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                 bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, 
                                 aliens, bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                      bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if not stats.game_active:
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statisttics
        stats.reset_stats()
        stats.game_active = True
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

# So if a mouse button is pressed down, we check if the position of the mouse
# is colliding with the button (is on the button), therefore mimicking the 
# clicking of a button

# Pygame detects a MOUSEBUTTONDOWN event when the player clicks anywhere on the
# screen. We use the conditional to restrict it to only the button.
# pygame.mouse.get_pos() returns a tuple containing the x- and y- coordinates
# of the mouse cursor when the mouse button is clicked.

# In larger projects, you'll often refactor code you've written before adding
# more code. Refactoring simplifies the structure of the code you've already
# written, making it easier to build on

# For example, we created a new module called game_function which will store
# a number of functions that make Alien Invasion work. The game_functions
# module will prevent alien_invasion.py from becoming too lengthy and will
# make the logic in alien_invasion.py to follow

# One issue with our play button is that the button region on the screen can
# always be clicked even when the button isn't there. Therefore, we add
# another conditional to ensure whether the game is actually running

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Redraw ship
    ship.blitme()
    # Redraw aliens
    aliens.draw(screen)
    # Draw the score information.
    sb.show_score()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently drawn screen visible.
    pygame.display.flip()

# We have now an updated screen for seamless movement

# Now, let's give the player the ability to move the ship right and left
# Whenever the player presses a key, that keypress is registered in Pygame
# as an event. Each event is picked up by the pygame.event.get() method,
# so we need to specify in our check_events() function what kind of events to
# check for. Each keypress is registered as a KEYDOWN event.

# When a KEYDOWN event is detected, we need to check whether the key that
# was pressed is one that triggers a certain event. For example, if the
# right arrow key is pressed, we increase the ship's rect.centerx value to
# move the ship to the right.

# We're gonna upgrade check_events for these key presses

# The function check_events seems to be too long, so we're gonna split it
# into 2 (actually 3).

# So now we put the bullet update. To everything together for bullets, we
# import the Bullet class and make an instance of it called new_bullet
# everytime we press the spacebar. This instance gets added to the bullets
# group. (So, now we have a list of class instances as Group instance called
# bullets). This alters the check_keydown_events function which alters
# the check_events function (more parameters for example, thanks to the Bullet
# class).

# In the update_screen function, it now pulls out every element in the bullets
# list (which is a bullet) and calls their draw_bullet method since they're
# class 

# Now, you must be wondering how do these bullets move. Let's look at 
# alien_invasion.py. 

# Note the order of object drawing in update_screen actually matters. It
# determines which object is in the front. If I put the for loop bullet lines
# ahead of ship.blitme() the bullets would be on top of the ship

# We're gonna add the bullet limitation (number of bullets allowed) into the
# K_SPACE event, so we can control how many bullets are drawn. If the length
# of bullets surpasses the amount of bullets allowed in the settings file (3)
# then, the program will stop adding new bullets into the bullets list.

# We're gonna try to keep alien_invasion.py as simple as possible which means
# extracting any extra lines from there and putting it into singular functions
# for better readability.

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, 
                                  bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, 
                                  bullets):
    """Respond to bullet-alien collsion."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

# Remember when groupcollide returns a dictionary? Each key in the dictionary
# is the first group's sprites or in this example, bullets while each value is
# the sprite that it collided with which are aliens in this case. The issue is
# that sometimes if two collisions happens at the same time, you'll only be
# rewarded with for one collision. To fix this, we take advantage of the
# groupcollide dictionary. The dictionary contains all of the collided aliens
# as values in its dictionary, so we just add up all of the values for each 
# bullet key to find out our true score. 

# The sprite.groupcollide() method compares each bullet's rect with each
# alien's rect and returns a dictionary containing the buellets and aliens
# that have collided. Each key in the dictionary is a bullet, and the
# corresponding value is the alien that was hit. The two True arguments tell
# Pygame whether to delete the bullets and aliens that have collided. If you
# set the first boolean argument as false. The bullets will not disappear and
# keep killing aliens.

# When you call draw() on a group (an instance of Group()), Pygame automatically
# draws each element in the group at the position defined by its rect attribute

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

    # This function starts off with setting variables for Alien instances and
    # alien_width. Then using our logic from before, it manages to find the
    # number of aliens that can fit in our available space

    # Now, we make a loop through the number of aliens and proceed to add the
    # alien in their respective locations. To do this, we use each alien's
    # range index as a part of our calculations. If we include an alien and
    # then a alien_width space for every iteration, we should get 2 * 
    # alien_width. If we multiply this product with their index number which
    # just happens to be the numeric element of the range funcion
    # (alien_number), we get how many alien spaces we should go before we draw
    # each alien. Don't forget to add alien_width to this new product due to
    # the margin. Then, we set the alien's rect x value to our final answer and
    # add the finalized alien to our group aliens.

# To finish the fleet, we're gonna need rows of these aliens. 
# Fortunately, making this happen is easier than making the first row.
# What we need is really just the number of rows we can fit. To find the number
# of rows, we first find the amount of available vertical space. So, we
# want a top margin of one alien_height and a bottom margin of two alien_heights
# the ship's height (we can't make the alien intersect with the ship right at
# the beginning). 
# Thus, available space y = screen_height - 3 * alien_height - ship_height.
# To get the number of rows available to these alien freaks, we just take
# the available space and divide it by 2 times the alien_height to accomodate
# for the alien and the alien_height space between them.

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien_ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    # The method spritecollideany() takes two arguements: a sprite and a
    # group. The method looks for any member of the group that's collided with
    # the sprite and stops looping through the group as it finds one. Here,
    # the group is aliens and ship is the sprite

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

# The sleep function from the time module pauses the game for its argument in
# seconds. We redrew the fleet and recentered the ship everytime the ship 
# was hit by an alien.

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()