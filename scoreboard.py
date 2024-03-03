import pygame
from enemy_snake import EnemySnake
import random

ALIGNMENT = "center"
FONT = ("Arial", 24)

class Scoreboard:

    def __init__(self, snake):
        self.score = 1
        self.snake = snake
        self.enemy_snakes = []
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 24)

    def draw_scoreboard(self, screen):
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_surface, (0, 0))

    def increase_score(self):
        self.score += 1
        if self.score % 2 == 0:
            # Increase speed based on score
            new_speed = 0.05 + self.score 

            # Ensure new_speed is not zero
            if new_speed == 0:
                new_speed = 1

            # Define the possible behaviors for the enemy snakes
            behaviors = ["chase_player", "chase_food", "random", "chase_enemy"]

            # Select a random behavior for the new enemy snake
            behavior = random.choice(behaviors)

            # Create a new enemy snake with the selected behavior
            new_enemy_snake = EnemySnake("red", new_speed, self.snake, behavior=behavior)
            self.enemy_snakes.append(new_enemy_snake)

    def game_over(self, screen):
        game_over_surface = self.font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_surface, (0, 0))