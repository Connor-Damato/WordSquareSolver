# NY Times Letter Boxed Puzzle Solver
# Preconditions: Assumes letters cannot be duplicated between sides, and that there is always an answer
# Outputs the shortest answer
# Written by: Connor Damato
# 1/30/2024

from functools import partial
import multiprocessing as mp
import time
import tkinter as tk

dictFileName = "updated_dict.txt"


def main():
    generateWindow()


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

    return list(answers)


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


def findPair(allWords, maxDepth, sides, pair, allSolutions, startingWords):
    if isComplete(pair, sides):
        allSolutions.append([i for i in pair])
        return
    if len(pair) == maxDepth:
        return
    if len(pair) == 0:
        for word in startingWords:
            findPair(
                removeSimilarWords(allWords, word),
                maxDepth,
                sides,
                [word],
                allSolutions,
                None,
            )
    else:
        for word in allWords:
            if eligibleWord(pair, word):
                pair.append(word)
                findPair(
                    removeSimilarWords(allWords, word),
                    maxDepth,
                    sides,
                    pair,
                    allSolutions,
                    None,
                )
                pair.remove(word)

    return


def lettersFromSides(sides):
    letters = []
    for side in sides:
        for letter in side:
            letters.append(letter)

    return letters


# sets the global allSolutions to every pair that solves the square.
# returns a list of the best solutions out of that global
def findBestSolution(sides, allSolutions, maxDepth):
    global foundDepth
    allPossibleWords = generateAllWords(sides)

    print(
        "Searching "
        + str(len(allPossibleWords))
        + " unique words for the best solution..."
    )

    # separate the list of all words to be run among the differnt cores of the CPU
    numCores = mp.cpu_count() - 4
    wordDiv = [[] for i in range(numCores)]
    for i in range(len(allPossibleWords)):
        wordDiv[i % numCores].append(allPossibleWords[i])

    pool = mp.Pool()
    pool.map_async(
        partial(findPair, allPossibleWords, maxDepth, sides, [], allSolutions),
        wordDiv,
    )
    pool.close()
    pool.join()

    allSolutions = sorted(allSolutions, key=lambda solution: len("".join(solution)))

    return [i for i in allSolutions if len("".join(i)) == len("".join(allSolutions[0]))]


def generateWindow():
    window = tk.Tk()
    window.title("Letter Boxed Solver")
    window.minsize(1040, 140)

    # where the words will be displayed
    frame_results = tk.Frame(
        master=window,
        width=200,
        height=100,
        bg="#ab9dac",
        relief=tk.SUNKEN,
        borderwidth=5,
    )
    # where the input will be placed
    frame_tools = tk.Frame(
        master=window,
        width=200,
        bg="#decee1",
        relief=tk.RAISED,
        borderwidth=3,
    )

    frame_tools.pack(fill=tk.BOTH, side=tk.LEFT)
    frame_results.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    results = tk.Text(master=frame_results, bg="#ab9dac", wrap="word")
    results_scroll = tk.Scrollbar(
        master=frame_results, orient="vertical", command=results.yview
    )
    results["yscrollcommand"] = results_scroll.set
    results.pack(expand=True, side="left", fill="both")
    results_scroll.pack(side="left", fill="y")

    results.insert(tk.END, "Waiting for input...")

    # forms the letter box
    entries = []
    for group in range(4):
        side = []
        for cell in range(3):
            entry = tk.Entry(master=frame_tools, width=3, font="Arial, 30")
            side.append(entry)
            if group == 0:
                entry.grid(row=group, column=cell + 1)
            elif group == 1:
                entry.grid(row=cell + 1, column=0)
            elif group == 2:
                entry.grid(row=cell + 1, column=4)
            else:
                entry.grid(row=group + 1, column=cell + 1)
        entries.append(side)
    depth = tk.Spinbox(master=frame_tools, from_=1, to_=5, width=10)
    depth.grid(row=7, column=2)

    # clears inputs and generated words
    def handle_clear(event):
        for group in entries:
            for textBox in group:
                textBox.delete(0, tk.END)
        results.delete("1.0", tk.END)

    # displays the newly generated words based on the current input
    def handle_submit(event):
        start_time = time.time()
        sides = []

        maxDepth = 2

        for i in range(4):
            sides.append(
                entries[i][0].get() + entries[i][1].get() + entries[i][2].get()
            )

        maxDepth = int(depth.get())
        manager = mp.Manager()
        allSolutions = manager.list()
        print(maxDepth, sides)
        bestAnswers = findBestSolution(sides, allSolutions, maxDepth)
        duration = time.time() - start_time
        print("Code Terminated- %.2f seconds." % duration)

        if allSolutions != []:
            addLabels(bestAnswers, allSolutions, results)

    # buttons
    btn_submit = tk.Button(master=frame_tools, text="Submit")
    btn_submit.grid(row=9, column=1, sticky="ew")

    btn_clear = tk.Button(master=frame_tools, text="Clear")
    btn_clear.grid(row=9, column=3, sticky="ew")

    # binds buttons/inputs to action listeners
    btn_clear.bind("<Button-1>", handle_clear)
    btn_submit.bind("<Button-1>", handle_submit)
    window.bind("<Return>", handle_submit)

    window.mainloop()


def addLabels(bestAnswers, allSolutions, results):
    results.tag_configure("bold", font="Helvetica 12 bold")
    results.delete("1.0", tk.END)
    results.insert(
        tk.END, "All Solutions of Depth " + str(len(allSolutions[0])) + ":\n", "bold"
    )
    results.insert(tk.END, allSolutions)

    results.insert(
        tk.END,
        "\nBest solution" + ("s: \n" if (not len(bestAnswers) == 1) else ": \n"),
        "bold",
    )
    results.insert(tk.END, bestAnswers)


if __name__ == "__main__":
    mp.freeze_support()
    main()
