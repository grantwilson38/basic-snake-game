import pygame
import math

SNAKE_SIZE = 10

STARTING_POSITIONS = [(x, 0) for x in range(0, -SNAKE_SIZE*3, -SNAKE_SIZE)]
MOVE_DISTANCE = 20
UP = (0, -MOVE_DISTANCE)
DOWN = (0, MOVE_DISTANCE)
LEFT = (-MOVE_DISTANCE, 0)
RIGHT = (MOVE_DISTANCE, 0)

class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, position, color=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=position)

class Snake:
    def __init__(self, color=(255, 255, 255)):
        self.segments = pygame.sprite.Group()
        self.create_snake(color)
        self.head = self.segments.sprites()[0]
        self.color = color
        self.direction = RIGHT

    def update(self, screen_width, screen_height, food):
        self.move()
        if self.head.rect.colliderect(food.rect):
            self.extend()
            food.create_new_food()
        return self.check_collision(screen_width, screen_height)

    def create_snake(self, color=(255, 255, 255)):
        for position in STARTING_POSITIONS:
            self.add_segment(position, color)

    def check_collision(self, screen_width, screen_height):
        if self.head.rect.left < 0 or self.head.rect.right > screen_width or \
        self.head.rect.top < 0 or self.head.rect.bottom > screen_height:
            return True

        for segment in self.segments.sprites()[1:]:
            if self.head.rect.colliderect(segment.rect):
                return True

    def move_towards_food(self, food):
        x_diff = food.rect.x - self.head.rect.x
        y_diff = food.rect.y - self.head.rect.y

        if abs(x_diff) > abs(y_diff):
            self.direction = RIGHT if x_diff > 0 else LEFT
        else:
            self.direction = DOWN if y_diff > 0 else UP

        self.move()

    def add_segment(self, position, color=(255, 255, 255)):
        new_segment = SnakeSegment(position, color)
        self.segments.add(new_segment)

    def extend(self):
        self.add_segment(self.segments.sprites()[-1].rect.topleft, self.color)

    def move(self):
        segments_list = list(self.segments.sprites())
        for seg_num in range(len(segments_list) - 1, 0, -1):
            segments_list[seg_num].rect = segments_list[seg_num - 1].rect.copy()
        self.head.rect.move_ip(self.direction[0], self.direction[1])

    def up(self):
        if self.direction != DOWN:
            self.direction = UP

    def down(self):
        if self.direction != UP:
            self.direction = DOWN

    def left(self):
        if self.direction != RIGHT:
            self.direction = LEFT

    def right(self):
        if self.direction != LEFT:
            self.direction = RIGHT

    def draw(self, screen):
        self.segments.draw(screen)