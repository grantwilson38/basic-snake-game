import pygame
import random
import sys
import time

from game_level import Level
from snake import Snake
from game_functions import play_again
from food import Food
from score import Score
from enemy_snake import EnemySnake

from miniboss import MiniBoss
from powerups import PowerUp

from game_over_screen import GameOverScreen

pygame.init()

# Create a font object
font = pygame.font.Font(None, 36)

# Define the game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SNAKE_SIZE = 10
FOOD_SIZE = 10

# Define the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load sounds
try:
    game_over_sound = pygame.mixer.Sound("Sounds/game_over.wav")
    game_start_sound = pygame.mixer.Sound("Sounds/game_start.wav")
    pellet_eat_sound = pygame.mixer.Sound("Sounds/pellet_eat.wav")
    scorpion_spawn_sound = pygame.mixer.Sound("Sounds/scorpion_spawn.mp3")
    miniboss_collision_sound = pygame.mixer.Sound("Sounds/miniboss_collision.wav")  # Water Bottle Crush by MysteryPancake -- https://freesound.org/s/434453/ -- License: Attribution 4.0
    power_up_sound = pygame.mixer.Sound("Sounds/power_up.wav")
except pygame.error as e:
    print("Error loading sound files:", e)
    sys.exit()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Create the game over screen
game_over_screen = GameOverScreen(screen, font, 600, 600, "You Lost", (255, 0, 0), 5000)

# Play the game start sound
game_start_sound.play()

# Pause the game for a few seconds
time.sleep(2)

# Create the snake, food, and scoreboard
snake = Snake()
food = Food(RED, FOOD_SIZE, FOOD_SIZE)

# Initialize player's lives
player_lives = 3

# Create a Level object
level = Level()

# Initialize the pellet counter
pellet_counter = 0

# Create a clock object
clock = pygame.time.Clock()

# Create the scoreboard
score = Score()

# Create the enemy snakes list
enemy_snakes = []  

def check_game_over(player_lives):
    if player_lives <= 0:
        return False, player_lives
    else:
        return True, player_lives

# Game loop
running = True
power_ups = [] # List to store active power-ups
spawn_power_up_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_power_up_event, 10000)  # Spawn a power-up every 10 seconds

while running:

    # Initialize the miniboss_spawned flag before the game loop
    miniboss_spawned = False

    screen.fill(BLACK)  # Fill the screen with black
    score.draw(screen)  # Draw the score
    level.draw(screen, font)  # Draw the level
    lives_surface = font.render(f"Lives: {player_lives}", True, (255, 255, 255))

    # Blit the lives surface to the screen
    screen.blit(lives_surface, (500, 10))

    # Check if the game is over
    running, player_lives = check_game_over(player_lives)

    # Handle the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.up()
            elif event.key == pygame.K_DOWN:
                snake.down()
            elif event.key == pygame.K_LEFT:
                snake.left()
            elif event.key == pygame.K_RIGHT:
                snake.right()

        elif event.type == spawn_power_up_event:
            # Spawn a new power-up at a random location
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            power_up_type = random.choice(["invincibility", "size_increase", "score_multiplier", "new_power_up_1", "new_power_up_2", "new_power_up_3", "new_power_up_4", "new_power_up_5", "new_power_up_6", "new_power_up_7", "new_power_up_8", "new_power_up_9", "new_power_up_10", "new_power_up_11", "new_power_up_12", "new_power_up_13", "new_power_up_14", "new_power_up_15", "new_power_up_16", "new_power_up_17", "new_power_up_18", "new_power_up_19", "new_power_up_20", "new_power_up_21", "new_power_up_22", "new_power_up_23", "new_power_up_24", "new_power_up_25", "new_power_up_26", "new_power_up_27", "new_power_up_28", "new_power_up_29", "new_power_up_30", "new_power_up_31", "new_power_up_32", "new_power_up_33", "new_power_up_34", "new_power_up_35", "new_power_up_36", "new_power_up_37", "new_power_up_38", "new_power_up_39", "new_power_up_40", "new_power_up_41", "new_power_up_42", "new_power_up_43", "new_power_up_44", "new_power_up_45", "new_power_up_46", "new_power_up_47", "new_power_up_48", "new_power_up_49", "new_power_up_50", "new_power_up_51", "new_power_up_52", "new_power_up_53", "new_power_up_54", "new_power_up_55"])
            new_power_up = PowerUp(power_up_type, (x, y), 5000)  # Assuming duration is in milliseconds
            power_ups.append(new_power_up)
    
    for power_up in power_ups:
        power_up.draw(screen)
        if power_up.check_collision_with_player(snake):
            power_up.apply_effect(snake)
            power_ups.remove(power_up)  # Remove the power-up after applying its effect

    snake.update(SCREEN_WIDTH, SCREEN_HEIGHT, food)  # Update the snake
    if food.update(snake):  # Update the food
        score.increase()
        pellet_counter += 1
        if pellet_counter % 1 == 0:
            level.increase()
        pellet_eat_sound.play()

    # Check for collision with enemy snakes
    for enemy_snake in enemy_snakes:
        if pygame.sprite.spritecollide(snake.head, enemy_snake.segments, False):
            game_over_sound.play()
            pygame.time.delay(4000)

            player_lives -= 1  # Decrease player's lives by 1

            if player_lives > 0:
                snake.respawn_player()  # Respawn the player's snake away from all enemy snakes
                enemy_snakes = []  # Remove all enemy snakes from the screen

    # Spawn a new enemy snake with a 3% chance
    if random.randint(1, 100) <= 3:
        color = (255, 0, 0)  # Red color
        speed = random.randint(3, 5)
        behavior = random.choice(["chase_player", "chase_food", "random", "chase_enemy"])
        size = random.randint(3, 5)

        enemy_snake = EnemySnake(color, speed, snake, behavior, size)
        enemy_snakes.append(enemy_snake)

    # Draw the game elements
    snake.draw(screen)
    food.draw(screen)
    for enemy_snake in enemy_snakes:
        enemy_snake.draw(screen)

    # Move the enemy snakes
    for enemy_snake in enemy_snakes:
        enemy_snake.move(food, enemy_snakes)
        if not enemy_snake.alive:
            enemy_snakes.remove(enemy_snake)

    # Update the mini boss's rect if the mini boss exists
    if level.miniboss is not None:
        level.miniboss.rect.x = level.miniboss.position[0]  # Access the x coordinate
        level.miniboss.rect.y = level.miniboss.position[1]  # Access the y coordinate

    # Assuming PowerUp is the class in powerups.py and it has the method check_collision_with_player
    for power_up in power_ups:  # Assuming power_ups is a list of PowerUp instances
        if power_up.check_collision_with_player(snake):  # Assuming snake has a position attribute
            # Handle collision
            power_up.apply_effect(snake)  # Apply the effect of the power-up
            power_ups.remove(power_up)

    # Update the display
    pygame.display.flip()

    # Check if the player has run into the walls or collided with an enemy snake
    if snake.check_collision(SCREEN_WIDTH, SCREEN_HEIGHT) or any(pygame.sprite.spritecollide(snake.head, enemy_snake.segments, False) for enemy_snake in enemy_snakes):
        game_over_sound.play()
        player_lives -= 1  # Decrease player's lives by 1
        pygame.time.delay(4000)
        # Check if the player has any lives left
        keep_playing, player_lives = play_again(screen, SCREEN_WIDTH, SCREEN_HEIGHT, player_lives)
        if running:
            snake.respawn_player()  # Respawn the player's snake away from all enemy snakes
            enemy_snakes = []  # Remove all enemy snakes from the screen

    # Separate check for collision with the miniboss
    if level.miniboss is not None and level.miniboss.rect.colliderect(snake.head.rect):
        miniboss_collision_sound.play()
        game_over_sound.play()
        player_lives -= 2 
        pygame.time.delay(4000)

        # Check if the player has any lives left after miniboss collision
        keep_playing, player_lives = play_again(screen, SCREEN_WIDTH, SCREEN_HEIGHT, player_lives)
        if running:
            snake.respawn_player() 
            enemy_snakes = []
            level.miniboss = None

    # Check if the player has run into the walls
    if snake.head.rect.left < 0 or snake.head.rect.right > SCREEN_WIDTH or \
       snake.head.rect.top < 0 or snake.head.rect.bottom > SCREEN_HEIGHT:
        game_over_sound.play()
        player_lives -= 1  # Decrease player's lives by 1

        snake.respawn_player()  # Respawn the player's snake away from all enemy snakes
        enemy_snakes = []  # Remove all enemy snakes from the screen
        
        if player_lives <= 0:
            running = False

    # Check if the level is three and the miniboss has not been created yet
    if level.level % 3 == 0 and level.miniboss is None and not miniboss_spawned: 
        scorpion_spawn_sound.play()
        level.miniboss = MiniBoss(SCREEN_WIDTH, SCREEN_HEIGHT)
        miniboss_spawned = True

    # If the miniboss exists, update and draw it
    if level.miniboss is not None:
        level.miniboss.update(snake.head.rect.center)
        level.miniboss.draw(screen)
        
        
    # Render the player's lives on the screen after they have been updated
    lives_surface = font.render(f"Lives: {player_lives}", True, (255, 255, 255))
    screen.blit(lives_surface, (500, 10))

    # Check if the game is over
    if not running:
        # Game over loop
        while not running:
            play_again_response = game_over_screen.ask_play_again()
            if play_again_response:
                # Reset the game state and start a new game
                running = True
                snake.respawn_player()
                enemies = []  # Clear the list of enemies
                bullets = []  # Clear the list of bullets
                score.reset()  # Reset the score
                player_lives = 3  # Reset the number of lives
            elif play_again_response is False:
                pygame.quit()
                sys.exit()
        
        # Process events in the game over loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(10)

# Game over
game_over_screen.display()
pygame.quit()
sys.exit()