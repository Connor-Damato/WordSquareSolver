# NY Times Letter Boxed Puzzle Solver
# Preconditions: Assumes letters cannot be duplicated between sides, and that there is always an answer
# Outputs the shortest answer
# Written by: Connor Damato
# 11/27/2023

allSolutions = []
dictFileName = "updated_dict.txt"


def main():
    sides = []

    for i in range(4):
        print("Enter the letters in side " + str(i + 1) + " as one string")
        sides.append(input())

    bestAnswers = findBestSolution(sides, allSolutions)
    print("All Solutions:")
    print(allSolutions)

    print("Best solution: ", end="")
    print(bestAnswers)


def letterToSide(letter, sides):
    side = 0
    for i in range(len(sides)):
        if letter in sides[i]:
            return i
    return side


def isNextPossibleLetter(prevLetter, currentLetter, sides):
    return letterToSide(prevLetter, sides) != letterToSide(currentLetter, sides)


def isLegalWord(word, sides):
    if len(word) < 3:
        return False

    for i in word:
        if i not in lettersFromSides(sides):
            return False

    for i in range(len(word)):
        if i != 0:
            if not isNextPossibleLetter(word[i - 1], word[i], sides):
                return False
    return True


def generateAllWords(sides):
    global dictFileName
    answers = set()
    file = open(dictFileName, "r")
    for word in file.read().split():
        if isLegalWord(word, sides):
            answers.add(word)

    return answers


# determines if a word can be appended to the pair
def eligibleWord(pair, word):
    if len(pair) != 0:
        return word[0] == pair[-1][-1]
    return True


def removeSimilarWords(allWords, word):
    remainingWords = set()
    for i in allWords:
        if i not in word:
            remainingWords.add(i)

    return remainingWords


# determines if the word pair is a complete answer and covers all the letters
def isComplete(pair, sides):
    letters = lettersFromSides(sides)
    return sorted(list(set("".join(pair)) & set(letters))) == sorted(letters)


def findPair(allWords, pair, currDepth, maxDepth, sides):
    global allSolutions
    if isComplete(pair, sides):
        allSolutions.append([i for i in pair])
        return
    if currDepth >= maxDepth:
        return
    for word in allWords:
        if eligibleWord(pair, word):
            pair.append(word)
            findPair(
                removeSimilarWords(allWords, word),
                pair,
                currDepth + 1,
                maxDepth,
                sides,
            )
            pair.remove(word)

    return


def lettersFromSides(sides):
    letters = []
    for side in sides:
        for letter in side:
            letters.append(letter)

    return letters


def findBestSolution(sides, allSolutions):
    allPossibleWords = generateAllWords(sides)
    print("Input the desired depth: ")
    maxDepth = int(input())

    print(
        "Searching "
        + str(len(allPossibleWords))
        + " unique words for the best solution..."
    )
    for i in range(maxDepth):
        print("Searching depth " + str(i + 1) + "...")
        findPair(allPossibleWords, [], 0, i + 1, sides)
        if (len(allSolutions)) != 0:
            break

    allSolutions = sorted(allSolutions, key=lambda solution: len("".join(solution)))

    return [i for i in allSolutions if len("".join(i)) == len("".join(allSolutions[0]))]


if __name__ == "__main__":
    main()
