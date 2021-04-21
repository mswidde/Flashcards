#
#   This file contains the data model and its functions
#
import common


class flashcards:
    def __init__(self):

        # cards is the full list of cards - each one is a dict
        # view is a (possbly filtered) list of indices for cards
        # skipped keeps track of questions marked as skipped
        self.cards = []
        self.view = []
        self.skipped = []

    # update view
    def updateView(self):

        # start with full list of indices, filter what we don't need
        self.view = [*range(0, len(self.cards))]

        # find skipped questions
        self.skipped = [
            crd
            for crd in self.view
            if "metadata" in self.cards[crd].keys()
            and self.cards[crd]["metadata"]["skip"] == "True"
        ]

        # filter based on display settings
        if common.ini["display"] == "Non-Skipped":
            self.view = list(set(self.view) - set(self.skipped))
        elif common.ini["display"] == "Skipped":
            self.view = [x for x in self.skipped]

        # filter based on search string
        if common.ini["search"]:
            input = common.ini["search"].lower()
            self.view = [
                x
                for x in self.view
                if input in self.cards[x]["question"].lower()
                or input in self.cards[x]["section"].lower()
                or input in self.cards[x]["subsection"].lower()
                or input in " ".join(self.cards[x]["answer"]).lower()
            ]

    # returns metadata skipped
    def getTagSkipped(self, currentcard) -> bool:
        return self.view[currentcard] in self.skipped

    # returns metadata thup
    def getThup(self, currentcard) -> bool:
        if "metadata" in self.cards[self.view[currentcard]].keys():
            return self.cards[self.view[currentcard]]["metadata"]["thup"]
        else:
            return 0

    # returns metadata thdn
    def getThdn(self, currentcard) -> bool:
        if "metadata" in self.cards[self.view[currentcard]].keys():
            return self.cards[self.view[currentcard]]["metadata"]["thdn"]
        else:
            return 0

    # increases metadata thup
    def incThup(self, currentcard) -> bool:

        # nothing to do if view is empty
        if self.view == []:
            return

        if "metadata" in self.cards[self.view[currentcard]].keys():
            self.cards[self.view[currentcard]]["metadata"]["thup"] = (
                self.cards[self.view[currentcard]]["metadata"]["thup"] + 1
            )
        else:
            self.cards[self.view[currentcard]]["metadata"] = {
                "skip": "False",
                "thup": 1,
                "thdn": 0,
            }

    # increases metadata thdn
    def incThdn(self, currentcard) -> bool:

        # nothing to do if view is empty
        if self.view == []:
            return

        if "metadata" in self.cards[self.view[currentcard]].keys():
            self.cards[self.view[currentcard]]["metadata"]["thdn"] = (
                self.cards[self.view[currentcard]]["metadata"]["thdn"] + 1
            )
        else:
            self.cards[self.view[currentcard]]["metadata"] = {
                "skip": "False",
                "thup": 0,
                "thdn": 1,
            }

    # toggles skip/unskip in metadata
    # returns a possibly updated current card
    def toggleSkip(self, currentcard) -> int:

        # nothing to do if view is empty
        if self.view == []:
            return 0

        prev = currentcard - 1 if currentcard > 0 else 0

        if "metadata" in self.cards[self.view[currentcard]].keys():
            if self.cards[self.view[currentcard]]["metadata"]["skip"] == "True":
                # unskip
                self.cards[self.view[currentcard]]["metadata"]["skip"] = "False"
                self.skipped.remove(self.view[currentcard])

                # if we were displaying only skipped cards, we must now remove it from the view
                # (note that we cannot be in the sit with display non-skipped, b/c the current card was originally skipped)
                if common.ini["display"] == "Skipped":
                    self.view.remove(self.view[currentcard])
                    return prev

            else:
                # skip
                self.cards[self.view[currentcard]]["metadata"]["skip"] = "True"
                self.skipped.append(self.view[currentcard])

                # if we were displaying only non-skipped cards, we must now remove it from the view
                # (note that we cannot be in the sit with display skipped, b/c the current card was originally non-skipped)
                if common.ini["display"] == "Non-Skipped":
                    self.view.remove(self.view[currentcard])
                    return prev
        else:
            self.cards[self.view[currentcard]]["metadata"] = {
                "skip": "True",
                "thup": 0,
                "thdn": 0,
            }
            self.skipped.append(self.view[currentcard])

            # if we were displaying only skipped cards, we must now remove it from the view
            # (note that we cannot be in the sit with display non-skipped, b/c the current card was originally skipped)
            if common.ini["display"] == "Skipped":
                self.view.remove(self.view[currentcard])
                return prev

        return currentcard

    # returns dict with the info from the specified card
    def getCard(self, currentcard) -> dict:

        # nothing to do if view is empty
        if self.view == []:
            return {}

        return (
            self.cards[self.view[currentcard]] if currentcard < len(self.view) else {}
        )

    # next card in the view
    def next(self, currcard) -> int:
        return currcard + 1 if len(self.view) > currcard + 1 else 0

    # previous card in the view
    def previous(self, currcard) -> int:
        return len(self.view) - 1 if currcard == 0 else currcard - 1

    # return total cards
    def totalCards(self) -> int:
        return len(self.cards)

    # return total cards in the view
    def totalView(self) -> int:
        return len(self.view)

    # returns total number of cards marked as skip
    def totalSkipped(self) -> int:
        return len(self.skipped)

    # load cards from a file
    def loadCards(self):

        # Create cards from the file
        try:
            self.cards = self.createCards()

            # merge cache with current set (if available)
            common.merge_cache()
        except:

            # if things went wrong we have zero cards
            self.cards = []

        # update view
        self.updateView()

    # parse text into cards
    def createCards(self) -> list:

        flashcards = []

        # read file and parse text lines into cards
        flashFile = open(common.ini["mdFile"], "r")
        inputText = flashFile.readlines()

        # First find all the last answers by looking at where the text indentation goes back
        current = 0
        last_answers = []
        for num, line in enumerate(inputText):

            # skip empty lines
            if line == "\n":
                if current > 0:
                    # mark last answer when level went down
                    current = 0
                    last_answers.append(num - 1)
                continue

            # skip sections
            if len(line) > 4 and line[0:3] == "###":
                if current > 0:
                    # mark last answer when level went down
                    current = 0
                    last_answers.append(num - 1)
                continue

            # other lines must start with a '-' after some leading spaces or tabs
            level = 0
            for c in line:
                if c == "-":
                    last_dashline = num
                    if current > level:
                        # mark last answer when level went down
                        current = 0
                        last_answers.append(num - 1)
                        break
                    else:
                        current = level
                        break
                elif c == " " or c == "\t":
                    level = level + 1

        # add last question (level did not go down because there was no next question)
        last_answers.append(last_dashline)

        # process last answers, make each into a flashcard
        for la in last_answers:

            answer = []
            question = ""
            subsection = ""
            section = ""

            # starting point
            scan = la
            level = len(inputText[scan].split("-")[0])

            # get lines with answer
            while len(inputText[scan].split("-")[0]) == level:
                answer.insert(0, inputText[scan].split("-", 1)[1])
                scan = scan - 1

            # next we must have arrived at the question
            level = len(inputText[scan].split("-")[0])
            question = inputText[scan].split("-")[1]

            # optional subsections
            if level > 0:
                # get line with subsection
                while len(inputText[scan].split("-")[0]) > 0:
                    scan = scan - 1
                subsection = inputText[scan].split("-")[1]

            # next we scan until we find the section
            while scan >= 0:
                if inputText[scan].startswith("###"):
                    section = inputText[scan].split("###")[1]
                scan = scan - 1

            card = {
                "section": section,
                "subsection": subsection,
                "question": question,
                "answer": answer,
            }
            flashcards.append(card)

        return flashcards
