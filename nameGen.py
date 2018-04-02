import markov
import os.path
import math

print('''
Hello, valued <GET_RELATIONSHIP>!
This is a simple markov-chain based name generator.
It takes one or multiple text file listing names and creates a Markov chain representation of each file.
Then it can generate names that sound (mostly!) like the ones from the files.
If you list more than one file, the generator will count those as first and second (and third and fourth, etc) names.
e.g. if you type:
first_names.txt last_names.txt
Then the generator will create two-word names corresponding to those files.
''')
filenames = list()
chains = list()
while True:
    fileListStr = input('Please enter one or more filenames: ')
    if not fileListStr:
        print('boi u deaf?? No file names found')
    else:
        break

filenames = fileListStr.strip().split(' ')
for name in filenames:
    print('Reading ' + name + '...')
    f = None
    try:
        f = open(name.strip())
    except FileNotFoundError:
        print('The file \'' + name + '\' does not exist, skipping')
        continue
    chain = markov.MarkovChain()
    for line in f:
        chain.munchData(line.strip().lower())
    f.close()
    chain.bakeProbabilities()
    chains.append(chain)
    print('... done!')

if len(chains) == 0:
    print("No markov chains were generated. Did you specify valid text files? Exiting anyway, sorry")
    exit()

helpString = '''Commands/controls are:
<enter> - pressing this generates a name with the last parameters/commands specified.
exit - quits the program.
help - prints these instructions.
x y - sets min and max string lengths to x and y respectively
'''
print('''Now just press enter to generate a name. You can also type the following commands:''')
print(helpString)

minLength = 1
maxLength = math.inf
while True:
    command = input('Enter a command or press enter: ')
    if command == 'exit':
        break
    if command == 'help':
        print(helpString)
        continue
    minMax = command.split(' ')
    if len(minMax) == 2:
        minLength = int(minMax[0])
        maxLength = int(minMax[1])
        continue
    result = ''
    for chain in chains:
        word = ''
        while len(word) < minLength or len(word) > maxLength:
            word = ''.join(list(chain.walkDataString()))
        result += word + ' '
    print(result)


# TODO create a simple command parsing system, your code is U N A E S T H E T I C
# TODO ^ allow the user to command-specify tokens (e.g. 'Mac' considered one data char for scottish names)
# TODO ^ allow e.g. multiple min max things, pair for each word
# TODO make more robust vs file errors, spelling or input mistakes. Right now is crashing when user looks at the screen wrong
# TODO petition Guido van Rossum for multi line comments in Python. guido pls
