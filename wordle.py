# wordle solver


def main():
    answers = []
    currentGuess = "*****"
    lettersToRemove = ""
    necessaryLetters = ""
    letterDict = {}

    print("Input the word with * for blank spaces to search: ")
    currentGuess = input().lower()
    print("Input letters to remove: ")
    lettersToRemove = input()
    print("Input any letters that must be in the word and are not already: ")
    necessaryLetters = input()

    for letter in necessaryLetters:
        print(
            "Input the locations the letter "
            + letter
            + " cannot be (separated by ',' no space):"
        )
        letterDict[letter] = [int(i) for i in input().split(",")]

    necessaryLetters += currentGuess.replace("*", "")

    answers = getAnswers(currentGuess, lettersToRemove, necessaryLetters, letterDict)

    print(answers)


def compare(word1, word2, lettersToRemove, necessaryLetters, letterDict):
    for i in range(5):
        if word1[i] != word2[i] and word1[i] != "*":
            return False
        elif word1[i] == "*" and word2[i] in lettersToRemove:
            return False
    for letter in necessaryLetters:
        if letter not in word2:
            return False
        elif letter not in word1:
            if word2.find(letter) in letterDict.get(letter):
                return False

        else:
            word2 = word2.replace(letter, "*", 1)
    return True


def getAnswers(currentGuess, lettersToRemove, necessaryLetters, letterDict):
    answers = set()

    file = open("updated_dict.txt", "r")
    for word in file.read().split():
        if len(word) != 5:
            continue
        if compare(
            currentGuess, word.lower(), lettersToRemove, necessaryLetters, letterDict
        ):
            answers.add(word.lower())

    return sorted(list(answers))


if __name__ == "__main__":
    main()
