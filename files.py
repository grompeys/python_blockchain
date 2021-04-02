# mode='r' Read Access Only
# mode='w' Write Access Only (overwrites the entire file)
# mode='r' +Read & Write Access
# mode='x' Write Access Only: Exclusive Creation, Fails if File Exists
# mode='a' Write Access Only: Append to End of File if it Exists
# mode='b' Open in Binary Mode (for Writing Binary Data)

f = open('demo.txt', mode='w')
f.write('Hello from Python\n')
f.close()

with open('demo.txt', mode='a') as f:
    f.write('This is a new line\n')

with open('demo.txt', mode='r') as f:
    # Read the entire file as one string
    # file_content = f.read()
    # print(file_content)

    # Read the entire file as a list of string
    # where each string is a line
    # file_lines = f.readlines()
    # print(file_lines)

    line = f.readline()
    while line:
        print(line)
        line = f.readline()
