from snake import Snake, STARTING_POSITIONS
from food import Food
from scoreboard import Scoreboard

import math
import random
import sys
import time

import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT

import winsound

game_over_sound = pygame.mixer.Sound("game_over.wav")
game_start_sound = pygame.mixer.Sound("game_start.wav")
pellet_eat_sound = pygame.mixer.Sound("pellet_eat.wav")

pygame.init()

# Define the game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SNAKE_SIZE = 10
FOOD_SIZE = 10

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window title
pygame.display.set_caption("Snake Game")

# Set the background color
screen.fill(BLACK)

# Update the display
pygame.display.flip()

# Play the game start sound
game_start_sound.play()

# Pause the game for a few seconds
time.sleep(2)

# Create the snake and food sprites and add them to their respective groups
snake = Snake()
food = Food(RED, FOOD_SIZE, FOOD_SIZE)

# Create the scoreboard
scoreboard = Scoreboard(snake)

# Create a clock object
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                snake.up()
            elif event.key == K_DOWN:
                snake.down()
            elif event.key == K_LEFT:
                snake.left()
            elif event.key == K_RIGHT:
                snake.right()

    # Draw the snake and food
    snake.draw(screen)
    food.draw(screen)
    
    # Update the snake and food
    snake.update(SCREEN_WIDTH, SCREEN_HEIGHT)
    food.update(snake)

    # Check for collisions between the snake and the food
    if pygame.sprite.spritecollide(snake.head, pygame.sprite.GroupSingle(food), False):
        food.create_new_food()
        snake.extend()
        scoreboard.increase_score()
        # Play pellet_eat.wav
        pellet_eat_sound.play()

    # Check for collisions with the screen boundaries
    if snake.head.rect.left < 0 or snake.head.rect.right > SCREEN_WIDTH or \
        snake.head.rect.top < 0 or snake.head.rect.bottom > SCREEN_HEIGHT:
         running = False
         game_over_sound.play()

    # Check for collisions with the snake's tail
    flat_segments = list(snake.segments.sprites())[1:] # Exclude the head    
    if pygame.sprite.spritecollide(snake.head, pygame.sprite.Group(*flat_segments), False):
        running = False
        game_over_sound.play()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(10)

# Quit Pygame
pygame.quit()
sys.exit()