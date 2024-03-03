import pygame
import math

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, position, color=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=position)

class Snake:
    def __init__(self, color=(255, 255, 255), speed=0.01):
        self.segments = pygame.sprite.Group()
        self.create_snake(color)
        self.head = self.segments.sprites()[0]
        self.color = color
        self.speed = speed
        self.direction = RIGHT
        self.x = 0
        self.y = 0
        self.position = (self.x, self.y)
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def update(self, screen_width, screen_height):
        self.move()
        self.x, self.y = self.position
        self.rect.x = self.x
        self.rect.y = self.y
        return self.check_collision(screen_width, screen_height)

    def create_snake(self, color=(255, 255, 255)):
        for position in STARTING_POSITIONS:
            self.add_segment(position, color)

    def check_collision(self, screen_width, screen_height):
        # Check for collision with screen boundaries
        if self.head.rect.left < 0 or self.head.rect.right > screen_width or \
        self.head.rect.top < 0 or self.head.rect.bottom > screen_height:
            return True

        # Check for collision with self
        for segment in self.segments.sprites()[1:]:  # Exclude the head
            if self.head.rect.colliderect(segment.rect):
                return True

    def move_towards_food(self, food):
        x_diff = food.rect.x - self.head.rect.x
        y_diff = food.rect.y - self.head.rect.y

        if abs(x_diff) > abs(y_diff):
            # Move horizontally
            if x_diff > 0:
                self.direction = RIGHT
            else:
                self.direction = LEFT
        else:
            # Move vertically
            if y_diff > 0:
                self.direction = UP
            else:
                self.direction = DOWN

        self.move()

    def add_segment(self, position, color=(255, 255, 255)):
        new_segment = SnakeSegment(position, color)
        self.segments.add(new_segment)

    def extend(self):
        self.add_segment(self.segments[-1].topleft, self.color)

    def move(self):
        # Convert the Group to a list
        segments_list = list(self.segments.sprites())

        # Update the position of the segments
        for seg_num in range(len(segments_list) - 1, 0, -1):
            segments_list[seg_num].rect = segments_list[seg_num - 1].rect.copy()

        # Update the position of the head
        self.head.rect.move_ip(self.direction[0] * MOVE_DISTANCE, self.direction[1] * MOVE_DISTANCE)

        # Update the x, y, and position attributes based on the position of the head
        self.x = self.head.rect.x
        self.y = self.head.rect.y
        self.position = (self.x, self.y)

    def up(self):
        self.direction = UP

    def down(self):
        self.direction = DOWN

    def left(self):
        self.direction = LEFT

    def right(self):
        self.direction = RIGHT

    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.rect(screen, self.color, segment)