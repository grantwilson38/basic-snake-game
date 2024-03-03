from snake import Snake
import pygame
import random
import math

# Initialize the mixer module
pygame.mixer.init()

# Load the sound file
enemy_spawn = pygame.mixer.Sound("enemy_spawn.mp3")

class EnemySnake(Snake):
    def __init__(self, color, speed, player_snake, behavior):
        super().__init__(color, speed)
        self.behavior = behavior

        # Set the head's position to a random point within the screen boundaries
        self.head.goto(random.randint(-280, 280), random.randint(-280, 280))

        # Move all body segments to the position of the head
        for segment in self.segments:
            segment.goto(self.head.position())

        # Ensure the enemy snake is not too close to the player's snake
        while self.head.distance(player_snake.head) < 50:
            self.head.goto(random.randint(-280, 280), random.randint(-280, 280))
            for segment in self.segments:
                segment.goto(self.head.position())

        enemy_spawn.play()

    def move(self, player_snake, food, enemy_snakes):
        if self.behavior == "chase_player":
            self.move_towards(player_snake.head)
        elif self.behavior == "chase_food":
            self.move_towards(food)
        elif self.behavior == "random":
            self.move_randomly()
        elif self.behavior == "chase_enemy":
            closest_enemy = min(enemy_snakes, key=lambda snake: self.head.distance(snake.head))
            self.move_towards(closest_enemy.head)

    def move_towards(self, target):
        # Check if target has xcor and ycor attributes
        if not hasattr(target, "xcor") or not hasattr(target, "ycor"):
            raise TypeError('Target must be an object with xcor and ycor methods, like a turtle.Turtle instance.')

        # Calculate the angle to the target
        angle = math.atan2(target.ycor() - self.head.ycor(), target.xcor() - self.head.xcor())
        # Set the heading to the angle
        self.head.setheading(math.degrees(angle))
        # Move the snake forward
        self.head.forward(self.speed)

    def move_randomly(self):
        # Set a random heading
        self.head.setheading(random.randint(0, 360))
        # Move the snake forward
        self.head.forward(self.speed)