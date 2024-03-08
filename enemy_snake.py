from snake import Snake
import pygame
import random
import math

# Define the directions
RIGHT = (1, 0)
LEFT = (-1, 0)
DOWN = (0, 1)
UP = (0, -1)

# Initialize the mixer module
pygame.mixer.init()

# Load the sound file
enemy_spawn = pygame.mixer.Sound("enemy_spawn.mp3")

class EnemySnake(Snake):
    def __init__(self, color, speed, player_snake, behavior):
        super().__init__(color)
        self.speed = speed
        self.behavior = behavior
        self.player_snake = player_snake

        # Set the head's position to a random point within the screen boundaries
        self.head.topleft = (random.randint(0, 560), random.randint(0, 560))

        # Ensure the enemy snake is not too close to the player's snake
        while self.head.inflate(20, 20).colliderect(player_snake.head.inflate(20, 20)):
            self.head.topleft = (random.randint(0, 560), random.randint(0, 560))

        enemy_spawn.play()

    def move(self, food, enemy_snakes):
        # Move the head of the snake based on the behavior
        if self.behavior == "chase_player":
            self.move_towards(self.player_snake.head)
        elif self.behavior == "chase_food":
            self.move_towards(food.rect)
        elif self.behavior == "random":
            self.move_randomly()
        elif self.behavior == "chase_enemy":
            closest_enemy = min(enemy_snakes, key=lambda snake: self.head.distance(snake.head))
            self.move_towards(closest_enemy.head)

        super().move()

    def move_towards(self, target):
        x_diff = target.x - self.head.x
        y_diff = target.y - self.head.y

        if abs(x_diff) > abs(y_diff):
            # Move horizontally
            if x_diff > 0:
                self.direction = RIGHT
            else:
                self.direction = LEFT
        else:
            # Move vertically
            if y_diff > 0:
                self.direction = DOWN
            else:
                self.direction = UP

    def move_randomly(self):
        # Set a random direction
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])