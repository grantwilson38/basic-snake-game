import pygame

class MiniBoss:
    def __init__(self, screen_height):
        # Initialize the mini boss's attributes (position, size, speed, etc.)
        self.position = [0, screen_height]  # Start at the bottom of the screen
        self.speed = 5
        self.frame = 0  # Add this line

        # Load the image
        sprite_sheet = pygame.image.load(r"C:\Users\grant\OneDrive\Documents\GitHub\snakeGame\scorpion-move.png")

        # Define the size and position of the sprites you want to extract
        sprite_rect1 = pygame.Rect(0, 0, 64, 64)  # For the first scorpion
        sprite_rect2 = pygame.Rect(64, 0, 64, 64)  # For the second scorpion

        # Extract the sprites
        self.image1 = sprite_sheet.subsurface(sprite_rect1)
        self.image2 = sprite_sheet.subsurface(sprite_rect2)

        # Get the size from the image
        self.size = self.image1.get_rect().size

    def draw(self, screen):
        # Draw the mini boss on the screen
        if self.frame % 2 == 0:
            screen.blit(self.image1, self.position)
        else:
            screen.blit(self.image2, self.position)

    def update(self):
        # Update the mini boss's position, check for collisions, etc.
        self.position[1] -= self.speed  # Move up
        self.frame += 1  # Add this line