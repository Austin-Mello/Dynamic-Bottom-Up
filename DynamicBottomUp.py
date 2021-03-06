import sys

#--------------------
#GLOBALS
#--------------------

#An array to assign spaces to their proper place in the phrase.
spaceSpot = []
#The dictionary. Filled in the makeDict() function.
Dictionary = []

#--------------------
#CLASSES
#--------------------

#Holds the last valid word's i and j positions.
class lastGood:
	def __init__(self):
		#i is initially zero. j is initially i(0).
		self.lastGoodi = 0
		self.lastGoodj = 0


#--------------------
#FUNCTIONS
#--------------------

#Fills the Dictionary global from a .txt file.
def makeDict():
	with open('diction10k.txt', 'r') as dictFile:
		for line in dictFile:
			Dictionary.append(line.strip())
	pass

#Confirms if a given substring of the phrase is a valid word.
def Dict(word):
	return word in Dictionary
	pass

#Discovers if a phrase is splittable into multiple smaller words.
def split(phrase, n):

	#Will track the position of the last valid word.
	goodArray = [lastGood()]
	#An iterator for goodArray
	k = 0

	#The primary iterator through the phrase. Used in the outer loop.
	i = goodArray[k].lastGoodi
	#The secondary iterator through the phrase. Used in the inner loop.
	j = goodArray[k].lastGoodj

	#Outer loop. Travels from the first to the n'th letter in the phrase.
	while i <= n:
		#Carries the result of the Dict() function call.
		validWord = False

		#Inner loop. Travels from the i'th to the n'th letter of the phrase.
		while j <= n:
			#Collect a substring of the total phrase from i to j.
			wordMaybe = phrase[i:j]
			
			#If it's a valid word, store the results, as well as its i and j
			#positions.
			if Dict(wordMaybe) == True:
				validWord = True

				goodArray.append(lastGood())
				k += 1
				goodArray[k].lastGoodi = i
				goodArray[k].lastGoodj = j
				
				#Jump i ahead to the start of the next potentially valid word.
				i += len(wordMaybe)
				spaceSpot.append(i)

				break
			j += 1

		#If i reached the end of the word and is still valid, you're done.
		if validWord == True and i == n:
			return True

		#If the word was invalid, back up to your previous valid word.
		#From there, the inner loop will continue as normal.
		if validWord == False:
			#Edge Case: If i is zero and j > n, you're done.
			if i == 0:
				return False

			i = goodArray[k].lastGoodi
			j = goodArray[k].lastGoodj
			del goodArray[-1]
			k -= 1
			j += 1
			del spaceSpot[-1]
	pass


if __name__ == '__main__':

	makeDict()

	#Iterator for identifying the current line of the text file.
	#Only really necessary for line 1, but there ya go.
	i = 0

	#Load up the classes and adjacency matrix.
	for lines in sys.stdin.read().splitlines():
		#Scrape off the first line.
		if i < 1:
			#Grabs the index.
			numLines = int(lines)
			i += 1

		else:
			#Pulls the lines one by one, analyzes them, and prints the result.
			sys.stdout.write('phrase' + str(i) + '\n')
			phrase = str(lines)
			print(phrase + '\n')
			length = len(phrase)

			#Calls the split() function, this is where the magic happens.
			valid = split(phrase, length)

			if valid == True:
				sys.stdout.write('YES, can split. \n')

				#Run through the spaceSpot list and insert spaces into the
				#phrase as necessary.
				for i in range(len(spaceSpot)):
					phrase = phrase[:spaceSpot[i] + i] + ' ' + phrase[spaceSpot[i] + i:]
				sys.stdout.write(phrase + '\n')

				#Clear spaceSpot in preparation for the next phrase.
				spaceSpot = []

			else:
				sys.stdout.write('NO, cannot split. \n')
				spaceSpot = []