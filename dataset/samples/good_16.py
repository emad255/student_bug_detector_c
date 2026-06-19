# good_16.py
def get_evens(numbers):
    return [n for n in numbers if n % 2 == 0]

result = get_evens([1, 2, 3, 4, 5, 6])
print(result)