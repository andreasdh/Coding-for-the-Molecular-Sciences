from turtle import *

shape("turtle")
color("limegreen")
speed(3)

number_of_sides = 6
side_length = 80
turning_angle = 360 / number_of_sides

for side in range(number_of_sides):
    forward(side_length)
    left(turning_angle)

done()
