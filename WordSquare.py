# NY Times Letter Boxed Puzzle Solver
# Preconditions: Assumes letters cannot be duplicated between sides, and that there is always an answer
# Outputs the shortest answer
# Written by: Connor Damato
# 11/27/2023

allSolutions = []


def main():
    sides = []

    for i in range(4):
        print("Enter the letters in side " + str(i + 1) + " as one string")
        sides.append(input())

    print(findBestSolution(sides, allSolutions))


def letterToSide(letter, sides):
    side = 0
    for i in range(len(sides)):
        if letter in sides[i]:
            return i
    return side


def isNextPossibleLetter(prevLetter, currentLetter, sides):
    return letterToSide(prevLetter, sides) != letterToSide(currentLetter, sides)


def isLegalWord(word, sides):
    for i in word:
        if i not in lettersFromSides(sides):
            return False

    for i in range(len(word)):
        if i != 0:
            if not isNextPossibleLetter(word[i - 1], word[i], sides):
                return False
    return True


def generateAllWords(sides):
    answers = set()
    file = open("dict.txt", "r")
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


def isShorter(solution, best):
    if len(solution) < len(best):
        return True
    elif len(solution) == len(best):
        return len("".join(solution)) < len("".join(best))

    return False


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

    bestSolution = allSolutions[0]

    print("Best solution: ", end="")
    for solution in allSolutions:
        if isShorter(solution, bestSolution):
            bestSolution = solution

    return bestSolution


if __name__ == "__main__":
    main()
