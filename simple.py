def plus_digit_func(a, b):
    print(a + b)


def f(func):
    print(f'{func.__name__[:-5]}_logic')
    func(2, 3)


if __name__ == '__main__':
    f(plus_digit_func)
