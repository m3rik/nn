"""In a game of Lingo, there is a hidden word, five characters long. 
The object of the game is to find this word by guessing, and in return 
receive two kinds of clues: 1) the characters that are fully correct, with 
respect to identity as well as to position, and 2) the characters that are 
indeed present in the word, but which are placed in the wrong position. 
Write a program with which one can play Lingo. Use square brackets to 
mark characters correct in the sense of 1), and ordinary parentheses to 
mark characters correct in the sense of 2). Assuming, for example, that 
the program conceals the word "tiger", you should be able to interact with 
it in the following way:

>>> import lingo
snake
Clue: snak(e)
fiest
Clue: f[i](e)s(t)
times
Clue: [t][i]m[e]s
tiger
Clue: [t][i][g][e][r]"""

# I still can't fully implement it
# It won't (fully) work with words that contain the same letter twice
# Eg. word = "alley" if the user enters "valley" (witch will be truncated 
# To "valle" by this program) it should return "v(a)[l](l)(e)" but it
# Instead returns "v(a)(l)(l)(e)" And I couldn't find a way to make it work
# But I think a solution would be to use regex, which means I'll have to
# Think of a different algorithm to implement. If you found a way to make
# It fully work, please, send me a pull request. I'd love to see your solu-
# tion

from random import randrange

# It's not too hard, but I'll comment anyway
def lingo(words):
	pass

#test
# lingo(['alley'])
lingo(['tiger', 'house', 'cigar', 'opera', 'modem', 'horse', 'plane', 'white'])