def main():
    dictFileName = "updated_dict.txt"

    print("Give all the letters: ", end="")
    letters = input()
    print("Give the necessary letter: ", end="")
    mustHave = input()
    answers = getWords(letters, mustHave, dictFileName)

    print(answers)


def isLegalWord(word, letters, mustHave):
    if mustHave not in word:
        return False
    for i in word:
        if i not in letters:
            return False

    return True


def getWords(letters, mustHave, dictFileName):
    answers = []
    file = open(dictFileName, "r")
    for word in file.read().split():
        if isLegalWord(word.lower(), letters.lower(), mustHave.lower()):
            answers.append(word)

    return sorted(answers, key=len)


if __name__ == "__main__":
    main()
