from pathlib import Path
import random
import tkinter as tk
from tkinter import messagebox

def loadJokes(filepath):
    if not filepath.exists():
        raise FileNotFoundError("Could not find joke dataset at: " + str(filepath))

    jokesList = []
    with filepath.open("r", encoding="utf-8") as jokeTextFile:
        for rawLine in jokeTextFile:
            cleanedLine = rawLine.strip()
            if not cleanedLine or "?" not in cleanedLine:
                continue
            setupPart, punchlinePart = cleanedLine.split("?", 1)
            setupText = setupPart.strip() + "?"
            punchlineText = punchlinePart.strip()
            if setupText and punchlineText:
                jokesList.append((setupText, punchlineText))

    if not jokesList:
        raise ValueError("randomJokes.txt contains no valid '?' separate jokes.")
    return jokesList
    
class RandomJokeGenerator:
    def __init__(self, rootWindow, jokesList):
        self.rootWindow = rootWindow
        self.rootWindow.title("Random Joke Generator")
        self.rootWindow.geometry("450x500")
        self.rootWindow.resizable(False, False)
        self.rootWindow.configure(bg="#FFF5F8")

        self.jokesList = jokesList
        self.currentJoke = None
        self.lastIndex = None

        self.rootWindow.grid_columnconfigure(0, weight=1)
        self.buildLayout()
