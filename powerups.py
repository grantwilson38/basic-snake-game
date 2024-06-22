import random
import os
import pygame
from snake import Snake
from score import Score

MOVE_DISTANCE = 20
SNAKE_SIZE = 10

UP = (0, -MOVE_DISTANCE)
DOWN = (0, MOVE_DISTANCE)
LEFT = (-MOVE_DISTANCE, 0)
RIGHT = (MOVE_DISTANCE, 0)

# Initialize Pygame
pygame.init()

class PowerUp:
    def __init__(self, type, position):
        super().__init__()
        self.type = type
        self.position = position
        self.visible = True  # Power-up is visible until picked up or duration ends
        self.active = True  # Power-up is active until picked up or duration ends
        # Load the image
        sprite_sheet = pygame.image.load(os.path.join("Images", "powerups.png")).convert_alpha()
        self.image = self.get_image(sprite_sheet)
        self.rect = self.image.get_rect(center=position)

    def get_image(self, sprite_sheet):
        # List of power-up types, expanded as needed
        power_up_types = ["invincibility", "size_increase", "score_multiplier"]
        index = power_up_types.index(self.type)
        row = index // 7  # 7 power-ups per row given the new sheet width
        col = index % 7

        # Calculate the subsurface rectangle for the power-up
        x = col * 32
        y = row * 32
        image = sprite_sheet.subsurface((x, y, 32, 32))
        return image
        
    def draw(self, screen):
        if self.type == "invincibility":
            color = (255, 255, 0)  # Yellow for invincibility
        elif self.type == "size_increase":
            color = (0, 0, 255)  # Blue for size increase
        elif self.type == "score_multiplier":
            color = (255, 0, 0)  # Red for score multiplier
        else:
            color = (255, 255, 255)  # Default color

        pygame.draw.circle(screen, color, self.position, 10)  # Draw a circle for the power-up 

    def check_collision_with_player(self, snake):
        # Check collision with each segment of the snake
        for segment in snake.segments:
            if self.rect.colliderect(segment.rect):
                power_up_sound = pygame.mixer.Sound(os.path.join("Sounds", "power_up.wav"))
                power_up_sound.play()
                return True
        return False

    def apply_effect(self, playerSnake, currentScore):
        # Apply the effect based on the power-up type
        if self.type == "invincibility":
            playerSnake.make_invincible()  # Make the snake invincible         

        elif self.type == "size_increase":
            # Add the first new segment
            last_segment = playerSnake.segments.sprites()[-1]
            if playerSnake.direction == UP:
                new_position = (last_segment.rect.x, last_segment.rect.y + SNAKE_SIZE)
            elif playerSnake.direction == DOWN:
                new_position = (last_segment.rect.x, last_segment.rect.y - SNAKE_SIZE)
            elif playerSnake.direction == LEFT:
                new_position = (last_segment.rect.x + SNAKE_SIZE, last_segment.rect.y)
            elif playerSnake.direction == RIGHT:
                new_position = (last_segment.rect.x - SNAKE_SIZE, last_segment.rect.y)
            playerSnake.add_segment(new_position, playerSnake.color)

            # Add the second new segment, adjusting the position calculation
            # Assuming the direction hasn't changed, we can use the same logic
            if playerSnake.direction == UP:
                new_position2 = (new_position[0], new_position[1] + SNAKE_SIZE)
            elif playerSnake.direction == DOWN:
                new_position2 = (new_position[0], new_position[1] - SNAKE_SIZE)
            elif playerSnake.direction == LEFT:
                new_position2 = (new_position[0] + SNAKE_SIZE, new_position[1])
            elif playerSnake.direction == RIGHT:
                new_position2 = (new_position[0] - SNAKE_SIZE, new_position[1])
            playerSnake.add_segment(new_position2, playerSnake.color)

        elif self.type == "score_multiplier":
            currentScore.double()

    def revert_effect(self, playerSnake):
        # Apply the effect based on the power-up type
        if self.type == "invincibility":
            Snake().make_vulnerable()  # Make the snake vulnerable
        elif self.type == "size_increase":
           pass
        elif self.type == "score_multiplier":
            pass