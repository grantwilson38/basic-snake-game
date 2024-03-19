from snake import Snake
import pygame
import random
import math

# Define game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

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
    def __init__(self, color, speed, player_snake, behavior, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__(color)
        self.speed = speed
        self.behavior = behavior
        self.player_snake = player_snake

        # Set the head's position to a random point within the screen boundaries
        self.head.rect.topleft = (random.randint(0, 560), random.randint(0, 560))

        # Ensure the enemy snake is not too close to the player's snake
        while self.head.rect.inflate(20, 20).colliderect(player_snake.head.rect.inflate(20, 20)):
            self.head.rect.topleft = (random.randint(0, 560), random.randint(0, 560))

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
            # Calculate the distance between the enemy snake's head and the head of each other snake
            other_enemies = [snake for snake in enemy_snakes if snake != self]
            closest_enemy = min(other_enemies, key=lambda snake: math.hypot(self.head.rect.x - snake.head.rect.x, self.head.rect.y - snake.head.rect.y))
            self.move_towards(closest_enemy.head.rect)

        super().move()

    def move_towards(self, target):
        if isinstance(target, pygame.Rect):
            target_x = target.x
            target_y = target.y
        else:  # target is a SnakeSegment object
            target_x = target.rect.x
            target_y = target.rect.y

        x_diff = target_x - self.head.rect.x
        y_diff = target_y - self.head.rect.y

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