#Create a random password generator with full functioning GUI and menu
'''
Generate a password,
Exit
'''

import random
import string

def generate_password():
    length = int(input("Enter password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choise(characters) for _ in range(length))
    print("Generated password:", password)

def main():
    while True:
        print("\nPassword Generator Menu")
        print("1. Generate a password")
        print("2. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            generate_password()
        elif choice == "2":
            print("Goodbye.")
            break
        else: print("Invalid choice. Try again.")

main()