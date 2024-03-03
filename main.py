from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time
import random
import pygame
import math

from snake import Snake, STARTING_POSITIONS
import winsound

game_over_sound = pygame.mixer.Sound("game_over.wav")
game_start_sound = pygame.mixer.Sound("game_start.wav")



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

# Initialize the screen
screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor(BLACK)
screen.title("Snake Game")
screen.tracer(0)

# Play the game start sound
game_start_sound.play()

# Pause the game for a few seconds
time.sleep(2)

# Create the player's snake, food, and scoreboard
snake = Snake(speed=0.1)
food = Food()
scoreboard = Scoreboard(snake)

# Listen for key presses
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

gameOn = True

counter = 0

while gameOn:
    screen.update()
    time.sleep(snake.speed)

    snake.move()

    # Detect collision with food for player's snake
    if snake.head.distance(food) < 15:
        food.create_food_random_color_random_location()
        snake.extend()
        scoreboard.increase_score()
        winsound.PlaySound("pellet_eat.wav", winsound.SND_ASYNC)

    # Detect collision with food for enemy snakes
    for enemy_snake in scoreboard.enemy_snakes:
        if enemy_snake.head.distance(food) < 15:
            food.create_food_random_color_random_location()
            enemy_snake.extend()

    # Move enemy snakes and check for collision
    for enemy_snake in scoreboard.enemy_snakes:
        enemy_snake.move(snake, food, scoreboard.enemy_snakes)
        if snake.head.distance(enemy_snake.head) < 10:
            gameOn = False
            game_over_sound.play()

    counter += 1

    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        gameOn = False
        scoreboard.game_over()
        game_over_sound.play()

    # Detect collision with tail
    for segment in snake.segments:
        if segment == snake.head:
            pass
        elif snake.head.distance(segment) < 10:
            gameOn = False
            scoreboard.game_over()
            game_over_sound.play()

    # Detect collision with enemy snake
    for enemy_snake in scoreboard.enemy_snakes:
        for segment in enemy_snake.segments:
            if snake.head.distance(segment) < 10:
                gameOn = False
                scoreboard.game_over()
                game_over_sound.play()

screen.exitonclick()
