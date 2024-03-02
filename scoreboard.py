from turtle import Turtle
from snake import Snake, STARTING_POSITIONS
import winsound
import pygame

# Initialize the mixer module
pygame.mixer.init()

# Load the sound file
enemy_spawn = pygame.mixer.Sound("enemy_spawn.mp3")

ALIGNMENT = "center"
FONT = ("Arial", 24, "normal")

class Scoreboard(Turtle):

    def __init__(self, snake):
        super().__init__()
        self.score = 0
        self.enemy_snakes = []
        self.snake = snake
        
        self.color("white")
        self.penup()
        self.goto(0, 260)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        if self.score % 2 == 0:
            new_enemy_snake = Snake("red", speed=0.05)
            while new_enemy_snake.head.distance(self.snake.head) < 50:  # Ensure the enemy snake is not too close
                new_enemy_snake = Snake("red", speed=0.025)
            self.enemy_snakes.append(new_enemy_snake)
            enemy_spawn.play()

        self.update_scoreboard()

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align=ALIGNMENT,font=FONT)