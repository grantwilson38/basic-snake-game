import random
import os
import pygame
from snake import Snake, make_invincible
from enemy_snake import EnemySnake

# Initialize Pygame
pygame.init()

class PowerUp:
    def __init__(self, type, position, duration):
        super().__init__()
        self.type = type
        self.position = position
        self.duration = duration
        self.visible = True  # Power-up is visible until picked up or duration ends
        self.active = True  # Power-up is active until picked up or duration ends
        # Load the image
        sprite_sheet = pygame.image.load(os.path.join("Images", "powerups.png")).convert_alpha()
        self.image = self.get_image(sprite_sheet)
        self.rect = self.image.get_rect(center=position)

    def get_image(self, sprite_sheet):
        # List of power-up types, expanded as needed
        power_up_types = ["invincibility", "size_increase", "score_multiplier", "new_power_up_1", "new_power_up_2", "new_power_up_3", "new_power_up_4", "new_power_up_5", "new_power_up_6", "new_power_up_7", "new_power_up_8", "new_power_up_9", "new_power_up_10", "new_power_up_11", "new_power_up_12", "new_power_up_13", "new_power_up_14", "new_power_up_15", "new_power_up_16", "new_power_up_17", "new_power_up_18", "new_power_up_19", "new_power_up_20", "new_power_up_21", "new_power_up_22", "new_power_up_23", "new_power_up_24", "new_power_up_25", "new_power_up_26", "new_power_up_27", "new_power_up_28", "new_power_up_29", "new_power_up_30", "new_power_up_31", "new_power_up_32", "new_power_up_33", "new_power_up_34", "new_power_up_35", "new_power_up_36", "new_power_up_37", "new_power_up_38", "new_power_up_39", "new_power_up_40", "new_power_up_41", "new_power_up_42", "new_power_up_43", "new_power_up_44", "new_power_up_45", "new_power_up_46", "new_power_up_47", "new_power_up_48", "new_power_up_49", "new_power_up_50", "new_power_up_51", "new_power_up_52", "new_power_up_53", "new_power_up_54", "new_power_up_55"]
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
            color = (0, 255, 0)  # Green for speed boost
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

    def apply_effect(self, player):
        # Apply the effect based on the power-up type
        if self.type == "invincibility":
            Snake.make_invincible()  # Make the snake invincible
        elif self.type == "size_increase":
            player.invincible = True  # Player cannot be harmed
        elif self.type == "speed_decrease":
            player.speed -= 2  # Decrease speed, but ensure it doesn't go below a minimum threshold
            if player.speed < 1:
                player.speed = 1
        elif self.type == "score_multiplier":
            player.score_multiplier += 2  # Double the score points gained
        # Add other effects based on the type

    def revert_effect(self, player):
        # Revert the effect based on the power-up type
        if self.type == "speed_boost":
            player.speed -= 2
        elif self.type == "invincibility":
            player.invincible = False
        elif self.type == "size_increase":
            player.size -= 1
        elif self.type == "speed_decrease":
            player.speed += 2  # Ensure to revert the speed decrease
        elif self.type == "score_multiplier":
            player.score_multiplier -= 2
        # Add reversion for other effects as necessary