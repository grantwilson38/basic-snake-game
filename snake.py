from turtle import Turtle
import random
import math

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:

    def __init__(self, color="white", speed=0.1):
        self.segments = []
        self.create_snake(color)
        self.head = self.segments[0]
        self.color = color
        self.speed = speed

    def create_snake(self, color="white"):
        for position in STARTING_POSITIONS:
            self.add_segment(position, color)

    def move_towards_food(self, food):
        x_diff = food.xcor() - self.head.xcor()
        y_diff = food.ycor() - self.head.ycor()

        if abs(x_diff) > abs(y_diff):
            # Move horizontally
            if x_diff > 0:
                self.head.setheading(RIGHT)
            else:
                self.head.setheading(LEFT)
        else:
            # Move vertically
            if y_diff > 0:
                self.head.setheading(UP)
            else:
                self.head.setheading(DOWN)

        self.move()

    def add_segment(self, position, color="white"):
        new_segment = Turtle("square")
        new_segment.color(color)
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend(self):
        self.add_segment(self.segments[-1].position(), self.color)

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.segments[0].forward(MOVE_DISTANCE)

    def up(self):
        self.head.setheading(UP)

    def down(self):
        self.head.setheading(DOWN)

    def left(self):
        self.head.setheading(LEFT)

    def right(self):
        self.head.setheading(RIGHT)
