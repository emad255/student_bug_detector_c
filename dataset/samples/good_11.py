try:
    number = int(input("Enter a number: "))
    print("Double:", number * 2)

except ValueError:
    print("Invalid input")