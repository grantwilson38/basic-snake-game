from turtle import Turtle
import random
import pygame

STARTING_POSITIONS = [(50, 50)]


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.all_foods = []
        self.create_food_random_color_random_location()

    def create_food(self):
        for position in STARTING_POSITIONS:
            self.create_new_food(position)

    def create_food_random_color_random_location(self):
        self.shape("circle")
        self.penup()
        self.shapesize(0.5, 0.5)
        random_color = random.choice(["red", "green", "blue"])
        self.color(random_color)
        self.speed("fastest")

        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)

    def multiply(self):
        new_food = self.clone()
        new_food.color("blue")

    def is_deadly(self):
        return self.color() == "white"

    def is_eaten(self, snake):
        if self.distance(snake.head) < 10:
            self.color("black")
            return True
        else:
            return False

    def eat(self, snake):
        if self.is_eaten(snake):
            snake.grow()
            self.create_food_random_color_random_location()

    def change_color(self):
        new_color = random.choice(["red", "green", "blue"])
        if new_color == self.color():
            new_color = random.choice(["red", "green", "blue"])
        self.color(new_color)

    def create_new_food(self, position):
        new_food = Turtle("square")
        new_food.color("white")
        new_food.penup()
        new_food.goto(position)
        self.all_foods.append(new_food)
