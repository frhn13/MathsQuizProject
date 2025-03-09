import random
from sympy import symbols, simplify, factor, expand

# Define the symbols
x = symbols('x')

# Define the algebra
expanded = 6*x**2 + 29*x + 35
factorised = (3*x + 7)*(2*x + 5)
simplified = (x**2 + 3*x + 2) / (x**2 + 5*x + 6)

simplified_fraction = simplify(simplified)

print(simplified_fraction)
print(factor(expanded))
print(expand(factorised))
# Generate a random factor
factor = (random.randint(1, 5))

# Create numerator and denominator with a common factor
numerator = factor * (x + random.randint(1, 5))
denominator = factor*3 * (x + random.randint(1, 5))

common_factor = random.randint(1, 3)

numerator = common_factor*random.randint(1, 3) * (x**2 * random.randint(1, 3) + x * random.randint(1, 3) + random.randint(1, 5))
denominator = common_factor * random.randint(1, 3) * (
x ** 2 * random.randint(1, 3) + x * random.randint(1, 3) + random.randint(1, 5))

def generate_expression():
    quadratic_value_added = True
    linear_value_added = True
    number_value_added = True

    quadratic_value = 0
    linear_value = 0
    number_value = 0

    if quadratic_value_added:
        quadratic_value = x**2 * random.choice([-3, -2, -1, 1, 2, 3])
    if linear_value_added:
        linear_value = x * random.choice([-3, -2, -1, 1, 2, 3])
    if number_value_added:
        number_value = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    return quadratic_value, linear_value, number_value

quadratic_value_numerator, linear_value_numerator, number_value_numerator = generate_expression()
quadratic_value_denominator, linear_value_denominator, number_value_denominator = generate_expression()

numerator = common_factor*random.randint(1, 3) * (quadratic_value_numerator + linear_value_numerator + number_value_numerator)
denominator = common_factor * random.randint(1, 3) * (
quadratic_value_denominator + linear_value_denominator + number_value_denominator)

print(numerator)
print(denominator)

print(type(numerator))
print(type(denominator))

frac = numerator / denominator
frac1 = simplify(numerator) / simplify(denominator)
print(simplify(frac))
print(type(frac))
print(numerator.as_ordered_terms()[0].coeff(x, numerator.as_ordered_terms()[0].as_poly().degree()))