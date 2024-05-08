def hello(): print(hello)


def calculator():
    print("Simple Calculator")
    print("Available operations: +, -, *, /")

    while True:
        operation = input("Enter an operation or 'q' to quit: ")

        if operation == 'q':
            print("Goodbye!")
            break

        if operation not in ('+', '-', '*', '/'):
            print("Invalid operation. Please try again.")
            continue

        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                print("Division by zero is not allowed.")
                continue
            result = num1 / num2

        print(f"Result: {result}\n")


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def long_list(a, b, c, d):
    long_param_1 = a
    long_param_2 = b
    long_param_3 = c
    long_param_4 = d

    return print(long_param_1, long_param_2, long_param_3,long_param_4)

