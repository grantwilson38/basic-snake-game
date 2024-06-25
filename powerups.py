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

power_up_indices = {
    "invincibility": 31,  # Index of invincibility power-up image in the sprite sheet
    "size_increase": 26,  # Index for size increase
    "score_multiplier": 49  # Index for score multiplier tilty sword
}

class PowerUp:
    def __init__(self, type, position, sprite_sheet):
        super().__init__()
        self.type = type
        self.position = position
        self.visible = True  # Power-up is visible until picked up or duration ends
        self.active = True  # Power-up is active until picked up or duration ends
        # Load the sprite sheet once and use it for all instances
        sprite_sheet_path = os.path.join("Images", "powerups.png")
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.image = self.get_image(sprite_sheet)
        self.rect = self.image.get_rect(center=position)

    def get_image(self, sprite_sheet):
        # Use the index from power_up_indices dictionary
        index = power_up_indices[self.type]
        row = index // 7  # Assuming 7 power-ups per row
        col = index % 7  # Assuming the sprite sheet layout matches

        # Calculate the subsurface rectangle for the power-up
        x = col * 32
        y = row * 32
        image = sprite_sheet.subsurface((x, y, 32, 32))
        return image
        
    def draw(self, screen):
        if self.visible:  # Only draw if the power-up is visible
            image_rect = self.image.get_rect(center=self.position)
            screen.blit(self.image, image_rect)

    def check_collision_with_player(self, snake):
        # Check collision with each segment of the snake
        for segment in snake.segments:
            if self.rect.colliderect(segment.rect):
                power_up_sound = pygame.mixer.Sound(os.path.join("Sounds", "power_up.wav"))
                self.visible = False  # Hide the power-up
                return True
        return False

    def apply_effect(self, playerSnake, currentScore):
        # Apply the effect based on the power-up type
        if self.type == "invincibility":
            # Apply the effect based on the power-up type
            if self.type == "invincibility":
                playerSnake.make_invincible()  # Make the snake invincible
                invincibility_sound = pygame.mixer.Sound(os.path.join("Sounds", "invincibility_sound.wav"))
                invincibility_sound.play()

        elif self.type == "size_increase":
            size_increase_sound = pygame.mixer.Sound(os.path.join("Sounds", "size_increase_sound.wav"))
            size_increase_sound.play()

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
            score_multiplier_sound = pygame.mixer.Sound(os.path.join("Sounds", "score_multiplier_sound.wav"))
            score_multiplier_sound.play()
            currentScore.double()

    def revert_effect(self, playerSnake):
        # Apply the effect based on the power-up type
        if self.type == "invincibility":
            Snake().make_vulnerable()  # Make the snake vulnerable
        elif self.type == "size_increase":
           pass
        elif self.type == "score_multiplier":
            pass