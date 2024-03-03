import pygame
import random

STARTING_POSITIONS = [(50, 50)]
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # red, green, blue

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
        if self.rect.colliderect(snake.rect):
            self.rect.topleft = random.choice(STARTING_POSITIONS)
            self.color = random.choice(COLORS)
            self.image.fill(self.color)
            snake.grow()

    def create_new_food(self, position):
        new_food = Food(self.color, self.rect.width, self.rect.height)
        new_food.rect.topleft = position
        return new_food