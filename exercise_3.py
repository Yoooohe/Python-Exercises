# define the function to calculate square root by babylonian method
# S is the number user enter to compute， x1，x2 are the factor of the S
def babylonian_method(S):
    x1 = 2
    x2 = S / x1
    while abs(x1 - x2) > 0.0001:
        x1 = (x1 + x2) / 2
        x2 = S / x1
    return x1

# Ask the user if they want to calculate square roots for a single value, or for a range of values.
single_or_range = input("Would you like to calculate a single or a range value(please enter 'single' or 'range'): ")

# user chooses to calculate the square root for a single value
if single_or_range == "single":
    single_value = int(input('Enter the integer number you want to compute square root (no negative number): '))
    while single_value <= 0:  # check validity (above zero)
        print('No negative number! ')
        single_value = int(input('Please try again: '))
    square_root = babylonian_method(single_value)
    print('The square root of', single_value, 'is: ', format(square_root, '.3f'))

# user chooses to calculate the square root for a range of value
elif single_or_range == "range":
    start_value = int(input('Enter the start integer number of the range you want to compute square root '
                            '(no negative number): '))
    end_value = int(input('Enter the end integer number you want to compute square root (no negative number): '))
    while (start_value <= 0) or (end_value <= 0):  # check validity (above zero)
        print('No negative number! ')
        start_value = int(input('the minimum of the range: '))
        end_value = int(input('the maximum of the range: '))
    print('Table of the square root is as following: ')
    for value in range(start_value, end_value + 1, 1):
        square_root = babylonian_method(value)
        num = str(value)
        print(num.rjust(5), format(square_root, '.3f').rjust(10), sep='', end='\n')

# user enter the informal answer
else:
    print('the value you enter is neither single nor range')


