import pygame
import sys

class GameOverScreen:
    def __init__(self, screen, font, width, height, text="Game Over", color=(255, 255, 255), wait_time=3000):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.wait_time = wait_time

    def display(self):
        game_over_text = self.font.render(self.text, True, self.color)
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        
    def ask_play_again(self):
        print("ask_play_again called") # Debugging
        self.text = "Game Over. Play Again? (Y/N)"
        self.display()  # Display the game over screen

        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  # If the "Y" key is pressed
                        return True
                    elif event.key == pygame.K_n:  # If the "N" key is pressed
                        return False