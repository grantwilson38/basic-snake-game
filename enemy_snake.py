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

        # Initialize some body segments for the enemy snake
        self.add_segment(self.head.position())
        for _ in range(3):
            self.add_segment(self.segments[-1].position())

        # Set the head's position to a random point within the screen boundaries
        self.head.goto(random.randint(-280, 280), random.randint(-280, 280))

        # Ensure the enemy snake is not too close to the player's snake
        while self.head.distance(player_snake.head) < 50:
            self.head.goto(random.randint(-280, 280), random.randint(-280, 280))

        enemy_spawn.play()

    def move(self, player_snake, food, enemy_snakes):
        # Move the head of the snake based on the behavior
        if self.behavior == "chase_player":
            self.move_towards(player_snake.head)
        elif self.behavior == "chase_food":
            self.move_towards(food)
        elif self.behavior == "random":
            self.move_randomly()
        elif self.behavior == "chase_enemy":
            closest_enemy = min(enemy_snakes, key=lambda snake: self.head.distance(snake.head))
            self.move_towards(closest_enemy.head)

        # Move each segment to the position of the segment ahead of it
        for seg_num in range(len(self.segments) - 1, 0, -1):
            self.segments[seg_num].goto(self.segments[seg_num - 1].xcor(), self.segments[seg_num - 1].ycor())

        # Move the first segment to the position of the head
        if len(self.segments) > 0:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

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
        new_heading = random.randint(0, 360)
        self.head.setheading(new_heading)

        # Check if the new heading would cause the snake to hit itself
        if len(self.segments) > 0:
            dx = self.segments[0].xcor() - self.head.xcor()
            dy = self.segments[0].ycor() - self.head.ycor()
            distance = math.sqrt(dx * dx + dy * dy)

            # If the new heading would cause the snake to hit itself, choose a new heading
            while distance < 20:
                new_heading = random.randint(0, 360)
                self.head.setheading(new_heading)
                dx = self.segments[0].xcor() - self.head.xcor()
                dy = self.segments[0].ycor() - self.head.ycor()
                distance = math.sqrt(dx * dx + dy * dy)

        # Move the snake forward
        self.head.forward(self.speed)