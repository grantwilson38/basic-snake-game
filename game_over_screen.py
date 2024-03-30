import pygame

# Define the game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class GameOverScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def display(self):
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before quitting