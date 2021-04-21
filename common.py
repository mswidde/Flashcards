#
#   This file contains the global variables and some common functions
#

import os
import json
import hashlib

# global vars
global myFlashcards
global ini

myFlashcards = None
ini = {}


# pick up the existing ini file (flashcards.json)
# if not available it creates a new one in the same folder as the python files
def load_ini():

    global ini

    # construct filename using the path for the python files
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # create hidden folder .flashcards if it doesn't exist
    # (note: folder won't be hidden in windows OS)
    cache_folder = dir_path + "/.flashcards"
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    filename = dir_path + "/.flashcards/ini.json"

    try:
        # load ini file
        ini = json.load(open(filename))

    except:

        # json not available / not properly formatted
        # setup a new default ini file
        ini = {"mdFile": "", "display": "non-skipped", "autonext": "True", "search": ""}
        save_ini()


# save ini
# used after changes or after reset to defaults
def save_ini():

    global ini

    # construct filename using the path for the python files
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = dir_path + "/.flashcards/ini.json"

    try:
        # save ini file
        with open(filename, "w") as outfile:
            json.dump(ini, outfile)

    except Exception as e:
        raise e


# tries to load cached json for current mdFile
def load_cache() -> dict:

    # construct filename based on hash of the path + name
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dirname, lastpart = ini["mdFile"].rsplit("/", 1)
    lastpart = lastpart.rsplit(".", 1)[0]
    md5hash = hashlib.md5(dirname.encode()).hexdigest()
    filename = f"{dir_path}/.flashcards/{md5hash}-{lastpart}.json"

    try:
        json_data = json.load(open(filename))
        return json_data
    except:
        return {}


# save cached json
# used after changes or after reset to defaults
def save_cache():

    # construct filename based on hash of the path + name
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dirname, lastpart = ini["mdFile"].rsplit("/", 1)
    lastpart = lastpart.rsplit(".", 1)[0]
    md5hash = hashlib.md5(dirname.encode()).hexdigest()
    filename = f"{dir_path}/.flashcards/{md5hash}-{lastpart}.json"

    try:
        # save current cards
        with open(filename, "w") as outfile:
            json.dump(myFlashcards.cards, outfile)

    except Exception as e:
        raise e


# delete cache data, create new cache
def clear_cache():

    # construct filename based on hash of the path + name
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dirname, lastpart = ini["mdFile"].rsplit("/", 1)
    lastpart = lastpart.rsplit(".", 1)[0]
    md5hash = hashlib.md5(dirname.encode()).hexdigest()
    filename = f"{dir_path}/.flashcards/{md5hash}-{lastpart}.json"

    try:
        # delete file
        os.remove(filename)
    except Exception as e:
        raise e


# update current cards by aligning with the cache metadata
def merge_cache():

    # starting point for inner loop / current cards
    # the idea is that although input files can be changed, the order of the q will usually remain the same
    # to start with where we found the previous q should speed up finding the match
    newstart = 0

    # pick up existing cache
    old_cache = load_cache()

    # if cached results then try to find/update corresponding meta data for current cards
    for crd_old in old_cache:

        # skip cards from cache that don't have metadata
        if "metadata" not in crd_old.keys():
            continue

        # loop over current cards with an index

        # start searching at point the last q was found (for performance)
        start = newstart
        for index in range(start, len(myFlashcards.cards)):

            if (
                myFlashcards.cards[index]["question"] == crd_old["question"]
                and myFlashcards.cards[index]["answer"] == crd_old["answer"]
                and myFlashcards.cards[index]["section"] == crd_old["section"]
                and myFlashcards.cards[index]["subsection"] == crd_old["subsection"]
            ):

                myFlashcards.cards[index]["metadata"] = crd_old["metadata"]
                newstart = index
                break

        # if not found yet, continue and complete the search from 0
        for index in range(0, start):
            if (
                myFlashcards.cards[index]["question"] == crd_old["question"]
                and myFlashcards.cards[index]["answer"] == crd_old["answer"]
                and myFlashcards.cards[index]["section"] == crd_old["section"]
                and myFlashcards.cards[index]["subsection"] == crd_old["subsection"]
            ):

                myFlashcards.cards[index]["metadata"] = crd_old["metadata"]
                newstart = index

    # align current/cache
    save_cache()
