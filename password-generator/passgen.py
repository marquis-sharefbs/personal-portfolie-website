# This is a password generator
# Able to generate a random string of characters of a given length

import string
import random

# Ask for password length in integer only
length = int(input("Enter desired length of password: "))

# Define set of characters to fill length of string
characters = string.ascii_letters + string.digits + string.punctuation

# Random pick and combination of characters from set
password = ''.join(random.choice(characters) for _ in range(length))

print("Your password is: ", password)
