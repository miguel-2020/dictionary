"""
    A simple dictionary application
    designed to provide you with quick and accurate word definitions.
"""
__version__ = '0.1'
__author__ = 'Miguel Ortiz'
import os
import sys
import json
import re

from difflib import get_close_matches
from typing import Dict,List
from pathlib import Path


path = Path('./dictionary.json')
type Matches = List[str]
type Dictionary = Dict[str,str]

def main():
    """Executes the dictionary application."""

    def run():
        dictionary = load_json()
        
        while True:
            word = input("Please enter the word or exit to end program: ")

            if word.lower() == 'exit':
                break

            isValidWord = re.search(r"^[a-zA-Z]+$",word,re.IGNORECASE)
            
            if not isValidWord:
                print("ERROR:Only characters from the alphabet are allow.")
                continue

            result = translate(word,dictionary)
            print("=" * 80)
            print(result)
            print("=" * 80)

    
    handle_errors(run)


def load_json() -> Dictionary:
    """loads a json file and returns a dictionary"""
    with open(path) as file:
        return json.load(file)
    

def handle_errors(callback):
    try:
        callback()

    except FileNotFoundError as file_error:
        # get the file name from path
        file_name = file_error.filename.split("/")[-1]
        print(f"ERROR: {file_error.strerror}: {file_name} could not be found.")

    except Exception as err:
        print("There was a problem running the program.")
        print(err)
        sys.exit(1)
    finally:
        print("Terminating program...")


def handle_matches(word:str,matches:Matches,dictionary:Dictionary) -> str:
    """Handles a list of the best "good enough" matches. """
    question = input(f"Did you mean {matches} ? Please Enter the correct word, or N if no: ").strip()

    match question:
        case question if question.isnumeric():
            return "ERROR:Only characters from the alphabet are allow."
        case 'N' | 'n':
            return "The word doesnt exist in this dictionary "
        case question if question != "":
            return dictionary[question]
        case _:
            return "We didn't understand your entry"
        

def translate(w:str,dictionary:Dict[str,str]) -> str:
    """handles dictionary queries and returns a string
    arguments:
    w-- the word to search for
    dictionary -- the dictionary for this application
    
    """
    word = w.lower()

    if word in dictionary:
        return dictionary[word]
    
    matches = get_close_matches(word,dictionary.keys())

    if(len(matches) > 0):
        return handle_matches(w,matches,dictionary)
        
    
    return "The word doesnt exist. Please double check it."


if __name__ == '__main__':
    main()


