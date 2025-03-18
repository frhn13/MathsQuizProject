import matplotlib.pyplot as plt
import random
from numpy import sqrt, degrees, rad2deg
from numpy.ma.core import arccos
from math import pi

# Angles in triangle. area and perimeter, pythagoras, SOHCAHTOA (trig), sine and cosine rule
def triangles_question_generation():
    pass

def find_angles(length_a, length_b, length_c):
    A = arccos((length_b**2 + length_c**2 - length_a**2) / (2*length_b*length_c))
    B = arccos((length_a**2 + length_c**2 - length_b**2) / (2*length_a*length_c))
    C = arccos((length_a**2 + length_b**2 - length_c**2) / (2*length_a*length_b))
    A = degrees(A)
    B = degrees(B)
    C = degrees(C)

    return A, B, C

def generate_triangle():
    while True:
        point_a = (random.randint(1, 10), random.randint(1, 10))
        point_b = (random.randint(1, 10), random.randint(1, 10))
        point_c = (random.randint(1, 10), random.randint(1, 10))
        if point_a != point_b and point_a != point_c and point_b != point_c and not \
            (point_a[0] == point_b[0] and point_a[0] == point_c[0]) and not (point_a[1] == point_b[1] and point_a[1] == point_c[1]):
            break

    return point_a, point_b, point_c

def draw(point_a, point_b, point_c):
    x_coordinates = [point_a[0], point_b[0], point_c[0], point_a[0]]
    y_coordinates = [point_a[1], point_b[1], point_c[1], point_a[1]]

    length_c = sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)
    length_b = sqrt((point_a[0] - point_c[0]) ** 2 + (point_a[1] - point_c[1]) ** 2)
    length_a = sqrt((point_b[0] - point_c[0]) ** 2 + (point_b[1] - point_c[1]) ** 2)

    perimeter = length_c + length_b + length_a
    angle_a, angle_b, angle_c = find_angles(length_a, length_b, length_c)

    plt.text((point_b[0] + point_c[0])/2, (point_b[1] + point_c[1])/2, f"Side a = {length_a}cm")
    plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b}cm")
    plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c}cm")

    plt.text(point_a[0], point_a[1], f"Angle A = {angle_a}°")
    plt.text(point_b[0], point_b[1], f"Angle B = {angle_b}°")
    plt.text(point_c[0], point_c[1], f"Angle C = {angle_c}°")

    print(point_a)
    print(point_b)
    print(point_c)
    print(perimeter)
    print(f"{angle_a}, {angle_b}, {angle_c}")

    plt.plot(x_coordinates, y_coordinates, color="blue", linestyle="-", marker=".")
    plt.show()


a, b, c = generate_triangle()
draw(a, b, c)