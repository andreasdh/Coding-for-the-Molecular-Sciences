from turtle import *
from random import choice

shape("turtle")
speed(0)
pensize(2)

possible_directions = [0, 90, 180, 270]
number_of_steps = 200
step_length = 10

dot(10, "red")  # Starting point

for step in range(number_of_steps):
    direction = choice(possible_directions)
    setheading(direction)
    forward(step_length)

dot(10, "blue")  # Final point
done()
