from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time
import random
import pygame

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


screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor(BLACK)
screen.title("Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
# newFood = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

gameOn = True
while gameOn:
    screen.update()
    time.sleep(0.1)

    snake.move()

    # Check if snake is eating food
    if snake.head.distance(food) < 15:
        food.create_food_random_color_random_location()
        snake.extend()
        scoreboard.increase_score()

    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        gameOn = False
        scoreboard.game_over()

    # Detect collision with tail
    for segment in snake.segments:
        if segment == snake.head:
            pass
        elif snake.head.distance(segment) < 10:
            gameOn = False
            scoreboard.game_over()

    # Detect if snake is eating old food



screen.exitonclick()
