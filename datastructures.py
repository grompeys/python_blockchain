list = [1,2,3,4]
list.extend([5,6,7])
del list[0]

print(list)

dictionary = {'name': 'Max'}
for k, v in dictionary.items():
    print(k, v)
del dictionary['name']
print(dictionary)

tuples = (1,2,3)
print(tuples.index(1))
# del tuples[0] won't work because tuples are immutable

set = {'Max', 'Anna'}
# del set['Max] won't work