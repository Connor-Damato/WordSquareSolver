# NYTimes Letter Boxed Solver!
This code produces the #1 answer(s) to a given letter boxed problem. The "best" answer to the puzzle is the answer that firstly- uses the least words, and secondly- uses the least letters.

## The rules of the game are as follows:
1. You must use every letter in the box at least once within the given limit of words.
2. Each word except your starting word must start with the last letter of the previous word.
  
   e.g. **space -> exploration** is valid, but **space -> ship** is not.
3. You cannot use a letter from the same side of the box twice in a row.

## An example Letter Boxed problem from the [NYT puzzle site](https://www.nytimes.com/puzzles/letter-boxed):
![image](https://github.com/Connor-Damato/WordSquareSolver/assets/67179143/6ef49ee6-40de-4d1a-8028-6744e237852f)

### To input into the program:
Enter the letters in side 1 as one string

jtr

Enter the letters in side 2 as one string

uih

Enter the letters in side 3 as one string

des

Enter the letters in side 4 as one string

myg

Input the desired depth:

3


**#note**: the order for each side does not matter, as long as each side is self contained. Case does not matter.

**#note**: Depth 3 should be the default depth unless you expect the puzzle will take more (an incredibly rare case). Most often, the solution will be within depth 2 (2 words required to generate a solution). 

### The output of the program:
All Solutions of Depth 2:

[['judger', 'rhythmist'], ['judger', 'rhythmists'], ['eurytherm', 'misjudge'], ['rejudge', 'erythrisms'], ['rejudge', 'erythrism'], ['judge', 'erythrisms'], ['judge', 'erythrism'], ['judgers', 'smithery'], ['judgers', 'smithy'], ['rhythm', 'misjudge'], ['misjudge', 'eurytherm'], ['misjudge', 'erythrite'], ['misjudge', 'eurytherms'], ['misjudge', 'erythrisms'], ['misjudge', 'erythrism'], ['erythrism', 'misjudge']]

Best solution: [['judgers', 'smithy']]

Code Terminated- 4.45 seconds.



#Final note: some words might not be accepted by the game, if encountered simply remove them from the updated_dict.txt file and rerun the script. Alternatively if an accepted word is not present in the file feel free to add it.

