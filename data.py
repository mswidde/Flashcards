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
                if input in self.cards[x]["Question"].lower()
                or input in self.cards[x]["Topic"].lower()
                or input in self.cards[x]["Section"].lower()
                or input in " ".join(self.cards[x]["Answer"]).lower()
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
    def incThup(self, currentcard):

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
    def incThdn(self, currentcard):

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

    # returns total number of cards with thup >0
    def totalwthup(self) -> int:

        totthup = 0
        for crd in self.cards:
            if "metadata" in crd.keys() and crd["metadata"]["thup"] > 0:
                totthup += 1

        return totthup

    # returns total number of cards with thup >0
    def totalwthdn(self) -> int:

        totthdn = 0
        for crd in self.cards:
            if "metadata" in crd.keys() and crd["metadata"]["thdn"] > 0:
                totthdn += 1

        return totthdn

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

        # read file into list of strings
        flashFile = open(common.ini["mdFile"], "r")
        inputText = flashFile.readlines()

        # first identify nature of each line: question, answer, section, topic
        line_id = ["" for i in range(len(inputText))]

        prev_indent = 0
        for line_index in range(len(inputText) - 1, -1, -1):

            cleanline = inputText[line_index].strip()

            # Topics
            if cleanline.startswith("###"):
                line_id[line_index] = "T"
                continue

            # Blank lines (or lines not starting with a - ), will be ignored later on
            if cleanline == "" or cleanline[0] != "-":
                line_id[line_index] = "B"
                continue

            # Q/A/S can be determined from indentation
            curr_indent = len(inputText[line_index].split("-")[0])
            if curr_indent >= prev_indent:
                line_id[line_index] = "A"
            elif line_id[line_index + 1] == "Q":
                line_id[line_index] = "S"
            else:
                line_id[line_index] = "Q"
                flashcards.append({})

            prev_indent = curr_indent

        # Now we can create the flashcards based on the line_id info
        topic = section = ""
        fc = -1
        for num, id in enumerate(line_id):

            if id == "B":
                continue

            if id == "T":
                topic = inputText[num].split("###")[1]
                continue

            if id == "S":
                section = inputText[num].split("-")[1]
                continue

            if id == "Q":
                fc += 1
                flashcards[fc]["Topic"] = topic
                flashcards[fc]["Section"] = section
                flashcards[fc]["Question"] = inputText[num].split("-", 1)[1]
                flashcards[fc]["Answer"] = []
                continue

            if id == "A":
                flashcards[fc]["Answer"].append(inputText[num].split("-", 1)[1])
                continue

        return flashcards
