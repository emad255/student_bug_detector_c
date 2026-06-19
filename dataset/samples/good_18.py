# good_18.py
def grade(score):
    if score >= 70:
        return "A"
    elif score >= 50:
        return "B"
    else:
        return "F"

print(grade(82))