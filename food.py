import pygame
import random

from events import PLAYER_EATS_FOOD

STARTING_POSITIONS = [(50, 50)]
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # red, green, blue
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FOOD_SIZE = 10

class Food(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.color = color
        self.image.fill(self.color)
        self.rect.topleft = random.choice(STARTING_POSITIONS)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, snake):
        if self.rect.colliderect(snake.head.rect):
            print("Food eaten")
            self.rect.topleft = random.choice(STARTING_POSITIONS)
            self.color = random.choice(COLORS)
            self.image.fill(self.color)
            snake.extend()
            pygame.event.post(pygame.event.Event(PLAYER_EATS_FOOD))
            return True
        return False

    def create_new_food(self, position=None):
        if position is None:
            position = self.get_random_position()
        self.rect.topleft = position
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.image.fill(self.color)
    
    def get_random_position(self):
        return (random.randint(0, SCREEN_WIDTH - FOOD_SIZE), random.randint(0, SCREEN_HEIGHT - FOOD_SIZE))