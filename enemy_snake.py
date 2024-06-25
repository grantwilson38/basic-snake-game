from snake import Snake, SnakeSegment
import pygame
import random
import math
import pygame.mixer
initialize = pygame.init()
enemy_eat = pygame.mixer.Sound("Sounds/enemy_eat.mp3")
enemy_death = pygame.mixer.Sound("Sounds/enemy_death.mp3")

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
enemy_spawn = pygame.mixer.Sound("Sounds/enemy_spawn.mp3")

class EnemySnake(Snake):
    def __init__(self, color, speed, player_snake, behavior, size):
        super().__init__(color)
        self.speed = speed
        self.behavior = behavior
        self.player_snake = player_snake
        self.alive = True
        self.size = size

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
            # Check for a collision with the food
            if pygame.sprite.collide_rect(self.head, food):
                enemy_eat.play()
                food.create_new_food()  # Spawn a new food
                # Add two new segments at the position of the last segment
                for _ in range(2):
                    self.add_segment(self.head.rect.topleft, self.color)

        elif self.behavior == "random":
            self.move_randomly()

        elif self.behavior == "chase_enemy":
            # Calculate the distance between the enemy snake's head and the head of each other snake
            other_enemies = [snake for snake in enemy_snakes if snake != self]
            if other_enemies:  # Check if other_enemies is not empty
                closest_enemy = min(other_enemies, key=lambda snake: math.hypot(self.head.rect.x - snake.head.rect.x, self.head.rect.y - snake.head.rect.y))
                self.move_towards(closest_enemy.head.rect)
            else:
                self.move_towards(self.player_snake.head)

        # Check for a collision with other enemy snakes
        for enemy in enemy_snakes:
            if enemy != self and pygame.sprite.spritecollide(self.head, enemy.segments, False):
                # Compare sizes to determine the outcome
                if self.size > enemy.size:
                    self.size += enemy.size  # Optionally increase the size of the bigger snake
                    enemy.alive = False  # Mark the smaller snake as dead
                    enemy_death.play()  # Play death sound for the smaller snake
                    # Add segments equivalent to the size of the eaten snake
                    for _ in range(enemy.size):
                        self.add_segment(self.head.rect.topleft, self.color)
                elif self.size < enemy.size:
                    self.alive = False  # This snake is smaller and gets eaten
                    enemy.size += self.size  # Optionally increase the size of the bigger snake
                    enemy_death.play()  # Play death sound for this snake
                break  # Exit the loop after handling collision

        # Check for collision with playerSnake's body
        for segment in self.player_snake.segments:
            if self.head.rect.colliderect(segment.rect):
                self.alive = False  # Mark the enemy snake as not alive
                enemy_death.play()  # Play death sound for this snake
                break  # Exit the loop as the enemy snake is now dead

        super().move()

    def add_segment(self, position, color):
        # Create a new segment
        new_segment = SnakeSegment(position, color)

        # If the snake has segments, add the new segment at the end of the snake
        if self.segments:
            last_segment = self.segments.sprites()[-1]
            new_segment.rect.topleft = (last_segment.rect.x - new_segment.rect.width, last_segment.rect.y)

        # Add the new segment to the segments group
        self.segments.add(new_segment)

    def move_towards(self, target):
        if isinstance(target, pygame.Rect):
            target_x = target.x
            target_y = target.y
        else:  # target is a SnakeSegment object
            target_x = target.rect.x
            target_y = target.rect.y

        x_diff = target_x - self.head.rect.x
        y_diff = target_y - self.head.rect.y
        distance = math.hypot(x_diff, y_diff)

        if distance > 0:
            x_diff, y_diff = x_diff / distance, y_diff / distance  # Normalize the direction vector (dx, dy)
            self.head.rect.x += x_diff * self.speed
            self.head.rect.y += y_diff * self.speed

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