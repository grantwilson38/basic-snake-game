import pygame
import math

# Define the starting positions for the snake segments
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]

# Define the move distance for the snake
MOVE_DISTANCE = 10

# Define the directions for the snake to move
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Define the SnakeSegment class that represents each segment of the snake
class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, position, color=(255, 255, 255)):
        super().__init__()
        # Create a surface for the segment and fill it with the specified color
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        # Get the rect of the surface and set its position to the specified position
        self.rect = self.image.get_rect(topleft=position)

# Define the Snake class
class Snake:
    def __init__(self, color=(255, 255, 255), speed=0.01):
        # Create a group to hold the segments of the snake
        self.segments = pygame.sprite.Group()
        self.create_snake(color)
        self.head = self.segments.sprites()[0]
        self.color = color
        self.speed = speed
        self.direction = RIGHT
        # Set the initial position of the snake
        self.x = 0
        self.y = 0
        self.position = (self.x, self.y)
        self.width = 20
        self.height = 20
        # Create a rect for the snake based on its position and size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # Update the snake's position and check for collisions
    def update(self, screen_width, screen_height):
        self.move()
        self.x, self.y = self.position
        self.rect.x = self.x
        self.rect.y = self.y
        return self.check_collision(screen_width, screen_height)

    # Create the initial segments of the snake
    def create_snake(self, color=(255, 255, 255)):
        for position in STARTING_POSITIONS:
            self.add_segment(position, color)

    # Check for collision with the screen boundaries or with itself
    def check_collision(self, screen_width, screen_height):
        # Check for collision with screen boundaries
        if self.head.rect.left < 0 or self.head.rect.right > screen_width or \
        self.head.rect.top < 0 or self.head.rect.bottom > screen_height:
            return True

        # Check for collision with self
        for segment in self.segments.sprites()[1:]:  # Exclude the head
            if self.head.rect.colliderect(segment.rect):
                return True

    # Move the snake towards the food position based on the x and y differences
    def move_towards_food(self, food):
        x_diff = food.rect.x - self.head.rect.x
        y_diff = food.rect.y - self.head.rect.y

        # Move horizontally if the x difference is greater than the y difference
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

    # Add a new segment to the snake at the specified position and color
    def add_segment(self, position, color=(255, 255, 255)):
        new_segment = SnakeSegment(position, color)
        self.segments.add(new_segment)

    # Increase the length of the snake by adding a new segment at the end
    def extend(self):
        self.add_segment(self.segments.sprites()[-1].rect.topleft, self.color)

    # Move the snake based on the current direction
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

    # Change the direction of the snake to up
    def up(self):
        self.direction = UP

    # Change the direction of the snake to down
    def down(self):
        self.direction = DOWN

    # Change the direction of the snake to left
    def left(self):
        self.direction = LEFT

    # Change the direction of the snake to right
    def right(self):
        self.direction = RIGHT

    # Draw the snake on the screen
    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.rect(screen, self.color, segment)