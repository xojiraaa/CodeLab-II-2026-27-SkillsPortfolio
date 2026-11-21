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