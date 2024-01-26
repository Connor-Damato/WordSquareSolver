# Word Generator Application
# Written by: Connor Damato
# Last Updated 1/26/24
#
# Letters to Use: All generated words don't contain any other letters besides these. Leave blank to have all letters used
# Necessary Letters: Similar to above, but if the letter(s) aren't in the word, then the word won't be added:
#   for example, if 'xy' all words would contain the letter 'x' and the letter 'y' somewhere
# Starts with: The letter/letters the word must start with: e.g. "hon" -> pyt"hon"
# Ends with: The letter/letters the word must end with: e.g. "py" -> "py"thon
# Contains: The group of letters that must be found in order somewhere in the word: e.g. "yth" -> p"yth"on
import tkinter as tk


def main():
    dictFileName = "updated_dict.txt"

    window = tk.Tk()
    window.title("Word Generator")
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
    frame_results.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    frame_tools.pack(fill=tk.BOTH, side=tk.LEFT)

    results = tk.Text(master=frame_results, bg="#ab9dac", wrap="word")
    results_scroll = tk.Scrollbar(
        master=frame_results, orient="vertical", command=results.yview
    )
    results["yscrollcommand"] = results_scroll.set
    results.pack(expand=True, side="left", fill="both")
    results_scroll.pack(side="left", fill="y")

    # inputs
    labels = [
        "Letters to Use:",
        "Necessary Letters:",
        "Starts With:",
        "End With:",
        "Contains:",
    ]
    entries = []
    for idx, text in enumerate(labels):
        label = tk.Label(master=frame_tools, text=text, bg="#decee1")

        entry = tk.Entry(master=frame_tools, width=35)
        entries.append(entry)
        label.grid(row=idx, column=0, sticky="e")
        entry.grid(row=idx, column=1)

    # clears inputs and generated words
    def handle_clear(event):
        for textBox in entries:
            textBox.delete(0, tk.END)
        results.delete("1.0", tk.END)

    # displays the newly generated words based on the current input
    def handle_submit(event):
        letters = entries[0].get()
        if letters == "":
            letters = "abcdefghijklmnopqrstuvwxyz"
        mustHave = entries[1].get()
        start = entries[2].get()
        end = entries[3].get()
        contains = entries[4].get()

        answers = getWords(letters, mustHave, dictFileName, start, end, contains)

        results.delete("1.0", tk.END)
        if answers != []:
            addLabels(answers, results)

    # buttons
    btn_submit = tk.Button(master=frame_tools, text="Submit")
    btn_submit.grid(row=idx + 1, column=1, sticky="ew")

    btn_clear = tk.Button(master=frame_tools, text="Clear")
    btn_clear.grid(row=idx + 1, column=0, sticky="ew")

    # binds buttons/inputs to action listeners
    btn_clear.bind("<Button-1>", handle_clear)
    btn_submit.bind("<Button-1>", handle_submit)
    window.bind("<Return>", handle_submit)

    window.mainloop()


# checks constraints
def isLegalWord(word, letters, mustHave, start, end, contains):
    # size of the word must be larger than the conditions
    if len(word) < len(contains) or len(word) < len(end) or len(word) < len(start):
        return False
    # must include these letters
    for i in mustHave:
        if i not in word:
            return False
    # can only use these letters
    for i in word:
        if i not in letters:
            return False
    # must contain this string
    if contains not in word:
        return False
    # must start with this string
    for i in range(len(start)):
        if word[i] != start[i]:
            return False
    # must end with this string
    for i in range(len(end)):
        if word[len(word) - len(end) + i] != end[i]:
            return False

    return True


# generates list of words based on constraints
def getWords(letters, mustHave, dictFileName, start, end, contains):
    answers = []
    file = open(dictFileName, "r")
    for word in file.read().split():
        if isLegalWord(
            word.lower(),
            letters.lower(),
            mustHave.lower(),
            start.lower(),
            end.lower(),
            contains.lower(),
        ):
            answers.append(word)

    return sorted(answers, key=len, reverse=True)


# displays the newly generated words on the screen with nice labels based on size (might add sorting options later)
def addLabels(words, results):
    results.tag_configure("bold", font="Helvetica 12 bold")
    minLen = len(words[0])
    results.insert("1.0", "Words with " + str(minLen) + " letters:\n", "bold")
    results.insert(tk.END, words[0] + " ")
    for i in range(len(words) - 1):
        if len(words[i + 1]) < minLen:
            minLen = len(words[i + 1])
            results.insert(
                tk.END, "\n\nWords with " + str(minLen) + " letters:\n", "bold"
            )
        results.insert(tk.END, words[i + 1] + " ")


if __name__ == "__main__":
    main()
