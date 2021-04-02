# The * means it will unpack the function's arguments
def unlimited_arguments(*args):
    for arg in args:
        print(arg)

unlimited_arguments(1,2,3,4)
# Same for the list
unlimited_arguments(*[1,2,3,4])

some_list = [1,2,3,4]

print('The list\'s elements are {} {} {} {}'.format(*some_list))

# We can also unpack named arguments with **
def unlimited_keyword_arguments(**kwargs):
    print(kwargs)
    for kw, arg in kwargs.items():
        print(kw, arg)

unlimited_keyword_arguments(firstname= 'Billy', lastname= 'Jimbob')