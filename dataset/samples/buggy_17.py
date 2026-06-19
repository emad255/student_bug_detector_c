# buggy_17.py
def countdown():
    n = 5
    while n > 0:
        print(n)
    # n is never decreased, so this loops forever

countdown()