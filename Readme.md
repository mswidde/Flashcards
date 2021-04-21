
# Flashcards

This is a simple Flashcards application written in Python. It uses the TKinter framework for the GUI. If you like my approach for taking notes you can use the program as-is and enjoy playing around / learn / study with the flashcards. Alternatively, you can study the code - either for the sake of adjjusting it to your needs or for just learning about Python/TKinter and about the code behind the program.

# Background

I used to write all my notes in OneNote. Recently however I changed my approach and I now write everything in simple markdown files, using Obsidian as my note-taking program. The reason I like markdown is that it's simple, text-based, fast and above all non-proprietary. 

For my notes I essentially use a very simple schema that goes like this:

```md
### Some header with the main topic of this section			-> main topic with triple hash sign
- A single line for the subsection							-> subsection is optional
	- A question											-> single line question
		- Answer line 1										-> multiline answer (can be one or more)
		- Answer line 2
		...
	- Another question
		- Answer

- Another subsection
	- Q
		- A

### Another topic
- Subsection
etc

```
Originally my 'questions' were not always phrased as such. Some were more like a lower-level topic I needed to know about and the answers then reflected what I should know. When the idea about turning my notes into flashcards started to emerge I rewrote them as real questions which was easy enough to do.

The flashcard program relies on the given structure to find related questions, answers, sections, and subsections.

# Options and keys

You can control some functions with keys:
- a for answer
- arrows left+right for previous and next question
- enter for putting the focus on the search button

The search function finds all substrings in all fields, including the answer field that may still be hidden. You can skip certain questions in the future by marking a question with the skip button. You can also mark them with thumbs up and thumbs down if you know or did not know the answer - so that you can get some idea of your progress.

All results are cached in a file (in a local folder called .flashcards). You can even switch to other files and come back later - results are cached for each file. The button Clear Results will only clear the cache for the current file.

# Example file
I included a small example markdown file you can play with.

# Screenshots

Question, answer hidden 
![Screenshot1](./ScreenShot1.png?raw=true "Without answer")

Question, answer shown
![Screenshot1](./ScreenShot2.png?raw=true "With the answer")

