from turtle import Turtle
from enemy_snake import EnemySnake
import random

ALIGNMENT = "center"
FONT = ("Arial", 24, "normal")

class Scoreboard(Turtle):

    def __init__(self, snake):
        super().__init__()
        self.score = 1
        self.snake = snake
        self.enemy_snakes = []
                
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
            # Increase speed based on score
            new_speed = 0.05 + self.score 

            # Ensure new_speed is not zero
            if new_speed == 0:
                new_speed = 1

            # Define the possible behaviors for the enemy snakes
            behaviors = ["chase_player", "chase_food", "random", "chase_enemy"]

            # Select a random behavior for the new enemy snake
            behavior = random.choice(behaviors)

            # Create a new enemy snake with the selected behavior
            new_enemy_snake = EnemySnake("red", new_speed, self.snake, behavior=behavior)
            self.enemy_snakes.append(new_enemy_snake)

        self.update_scoreboard()

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align=ALIGNMENT,font=FONT)