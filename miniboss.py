import pygame
import random

# Initialize Pygame
pygame.init()

# Load the sound files
enemy_death = pygame.mixer.Sound("Sounds/enemy_death.mp3")

class MiniBoss:
    def __init__(self, screen_width, screen_height):
        # Initialize the mini boss's attributes (position, size, speed, etc.)
        self.position = [random.randint(0, screen_width), screen_height]  # Start at the bottom of the screen
        self.speed = random.randint(3, 10)  # Random speed between 3 and 10
        self.size = (64, 64)  # Size of the miniboss
        self.frame = 0 # To keep track of the current frame
        self.alive = True  # To keep track of whether the miniboss is alive or not

        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

        # Load the image
        sprite_sheet = pygame.image.load("Images\scorpion-move.png")

        # Define the size and position of the sprites you want to extract
        sprite_rect1 = pygame.Rect(0, 0, 64, 64)  # For the first scorpion
        sprite_rect2 = pygame.Rect(64, 0, 64, 64)  # For the second scorpion
        sprite_rect3 = pygame.Rect(128, 0, 64, 64)
        sprite_rect4 = pygame.Rect(192, 0, 64, 64)

        # Extract the sprites
        self.image1 = sprite_sheet.subsurface(sprite_rect1)
        self.image2 = sprite_sheet.subsurface(sprite_rect2)
        self.image3 = sprite_sheet.subsurface(sprite_rect3)
        self.image4 = sprite_sheet.subsurface(sprite_rect4)

        # Get the size from the image
        self.size = self.image1.get_rect().size

    def draw(self, screen):
        if not self.alive:
            return
        else:
            # Draw the mini boss on the screen
            if self.frame % 4 == 0:
                screen.blit(self.image1, self.position)
            elif self.frame % 4 == 1:
                screen.blit(self.image2, self.position)
            elif self.frame % 4 == 2:
                screen.blit(self.image3, self.position)
            else:  # self.frame % 4 == 3
                screen.blit(self.image4, self.position)

    def update(self, player_position, playerSnake):
        if not self.alive:
            return False
        else:
            # Calculate the direction vector from the miniboss to the player
            dx = player_position[0] - self.position[0]
            dy = player_position[1] - self.position[1]
        
            # Normalize the direction vector (make its length 1)
            length = (dx**2 + dy**2)**0.5
            if length > 0:  # Avoid division by zero
                dx /= length
                dy /= length
        
            # Update the miniboss's position
            self.position[0] += dx * self.speed
            self.position[1] += dy * self.speed

            # Increment the frame
            self.frame += 1

            # Update the miniboss's rect position for accurate collision detection
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

            # Check for collision with the player snake
            if self.rect.colliderect(playerSnake.head.rect):
                if playerSnake.invincible:
                    self.alive = False
                    enemy_death.play()  # Play the death sound

                else:
                    # If the player is not invincible, the player dies
                    print("Player was hit by miniboss!")
                    return True