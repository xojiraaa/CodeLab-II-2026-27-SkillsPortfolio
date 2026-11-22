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

def clearContainer(self, targetContainer):
        for childWidget in targetContainer.winfo_children():
            childWidget.destroy()

def buildLayout(self):
        self.clearContainer(self.rootWindow)

        mainFrame = tk.Frame(self.rootWindow, bg="#FFF5F8", padx=22, pady=18)
        mainFrame.grid(row=0, column=0, sticky="nsew")
        mainFrame.grid_columnconfigure(0, weight=1)

        headerBox = tk.Frame(mainFrame, bg="#FAD2E1", highlightthickness=0, bd=0, relief=tk.FLAT, padx=12, pady=10)
        headerBox.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        headerBox.grid_columnconfigure(0, weight=1)

        tk.Label(headerBox, text="Lei's Random Joke Generator", font=("Arial", 15, "bold"), bg="#FAD2E1", fg="#85593E").grid(row=0, column=0)
        tk.Label(headerBox, text="powered by Alexa", font=("Arial", 9, "italic"), bg="#FAD2E1", fg="#85593E").grid(row=1, column=0, pady=(2, 0))

        jokeCard = tk.Frame(mainFrame, bg="#FFEBF2", highlightthickness=0, bd=0, relief=tk.FLAT, height=175, padx=16, pady=18)
        jokeCard.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        jokeCard.grid_propagate(False)
        jokeCard.grid_columnconfigure(0, weight=1)
        jokeCard.grid_rowconfigure(0, weight=1)

        jokeTextFrame = tk.Frame(jokeCard, bg="#FFEBF2")
        jokeTextFrame.grid(row=0, column=0)
        jokeTextFrame.grid_columnconfigure(0, weight=1)

        self.setupLabel = tk.Label(jokeTextFrame, text="Ready to laugh?\nClick the button below to start!", font=("Arial", 15), bg="#FFEBF2", fg="#85593E", wraplength=360, justify="center")
        self.setupLabel.grid(row=0, column=0)

        self.punchlineLabel = tk.Label(jokeTextFrame, text="", font=("Arial", 11, "italic", "bold"), bg="#FFEBF2", fg="#85593E", wraplength=360, justify="center")
        self.punchlineLabel.grid(row=1, column=0, pady=(10, 0))

        buttonFrame = tk.Frame(mainFrame, bg="#FFF5F8")
        buttonFrame.grid(row=2, column=0, sticky="ew")
        buttonFrame.grid_columnconfigure(0, weight=1)
        buttonFrame.grid_columnconfigure(1, weight=1)

        self.tellJokeButton = tk.Button(buttonFrame, text="Alexa tell me a Joke..", font=("Arial", 10, "bold"), bg="#FAD2E1", fg="#85593E", activebackground="#F5BAD0", activeforeground="#85593E", highlightbackground="#85593E", highlightthickness=4, relief=tk.GROOVE, bd=4, padx=10, pady=10, command=self.showRandomJoke)
        self.tellJokeButton.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        self.punchlineButton = tk.Button(buttonFrame, text="Show Punchline", font=("Arial", 10), bg="#FAD2E1", fg="#85593E", activebackground="#F5BAD0", activeforeground="#85593E", highlightbackground="#85593E", highlightthickness=4, relief=tk.GROOVE, bd=4, padx=10, pady=9, state=tk.DISABLED, command=self.showPunchline)
        self.punchlineButton.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 8))

        self.nextJokeButton = tk.Button(buttonFrame, text="Next Joke", font=("Arial", 10), bg="#FAD2E1", fg="#85593E", activebackground="#F5BAD0", activeforeground="#85593E", highlightbackground="#85593E", highlightthickness=4, relief=tk.GROOVE, bd=4, padx=10, pady=9, state=tk.DISABLED, command=self.showRandomJoke)
        self.nextJokeButton.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(0, 8))

        self.quitButton = tk.Button(buttonFrame, text="Quit", font=("Arial", 10, "bold"), bg="#FAD2E1", fg="#85593E", activebackground="#F5BAD0", activeforeground="#85593E", highlightbackground="#85593E", highlightthickness=4, relief=tk.GROOVE, bd=4, padx=10, pady=9, command=self.rootWindow.destroy)
        self.quitButton.grid(row=2, column=0, columnspan=2, sticky="ew")

def pickJoke(self):
        if len(self.jokesList) == 1:
            self.lastIndex = 0
            return self.jokesList[0]

        jokeOption = [jokeIndex for jokeIndex in range(len(self.jokesList)) if jokeIndex != self.lastIndex]
        chosenIndex = random.choice(jokeOption)
        self.lastIndex = chosenIndex
        return self.jokesList[chosenIndex]

def showRandomJoke(self):
        self.currentJoke = self.pickJoke()
        setupText, _ = self.currentJoke

        self.setupLabel.config(text=setupText)
        self.punchlineLabel.config(text="")
        self.punchlineButton.config(state=tk.NORMAL)
        self.nextJokeButton.config(state=tk.NORMAL)

def showPunchline(self):
        if self.currentJoke is None:
            return
        _, punchlineText = self.currentJoke
        self.punchlineLabel.config(text=str(punchlineText) + "\n😂😂😂")
        self.punchlineButton.config(state=tk.DISABLED)

def main():