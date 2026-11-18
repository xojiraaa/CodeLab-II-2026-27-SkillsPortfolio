import tkinter as tk
from random import randint, choice

root = tk.Tk()
root.geometry("450x450")
root.title("Arithmetic Maths Quiz")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)

totalQuestions = 10

difficultyRanges = {
    "easy": (1, 9),
    "moderate": (10, 99),
    "advanced": (1000, 9999),
}

difficultyLevel = "easy"
currentAnswer = 0
score = 0
questionCount = 1
attempts = 1
locked = False
pendingJob = None

givenAnswer = tk.StringVar()
checkAnswerText = tk.StringVar()
pointsText = tk.StringVar()
totalScoreText = tk.StringVar()

checkAnswerLabel = None
answerEntry = None
submitButton = None

def randomInt(level):
    minValue, maxValue = difficultyRanges[level]
    return randint(minValue, maxValue)

def decideOperation():
    return choice(['+', '-'])

def generateQuestion(level):
    num1 = randomInt(level)
    num2 = randomInt(level)
    operation = decideOperation()

    if operation == '+':
        answer = num1 + num2
    else:
        answer = num1 - num2

    questionText = str(num1) + " " + operation + " " + str(num2) + " ="
    return questionText, answer

def clearScreen():
    for widget in root.winfo_children():
        widget.destroy()

def cancelPendingJob():
    global pendingJob, locked
    if pendingJob is not None:
        root.after_cancel(pendingJob)
        pendingJob = None
    locked = False

def displayMenu():
    cancelPendingJob()
    clearScreen()

    headerLabel = tk.Label(root, text="Arithmetic Maths Quiz", font=("Trebuchet MS", 29, "bold"), fg="#123456")
    headerLabel.grid(row=0, column=0, pady=(20, 15))

    headerTitle = tk.Label(root, text="Difficulty Level", font=("Trebuchet MS", 18, "bold"), fg="#333333")
    headerTitle.grid(row=1, column=0, pady=(20, 15))

    easyButton = tk.Button(root, text="Easy", font=("Trebuchet MS", 12, "bold"), fg="#52a447",
                           command=lambda: startQuiz("easy"))
    easyButton.grid(row=3, column=0, pady=8)

    moderateButton = tk.Button(root, text="Moderate", font=("Trebuchet MS", 12, "bold"), fg="#ffbd31",
                               command=lambda: startQuiz("moderate"))
    moderateButton.grid(row=4, column=0, pady=8)

    advancedButton = tk.Button(root, text="Advanced", font=("Trebuchet MS", 12, "bold"), fg="#e50e0e",
                               command=lambda: startQuiz("advanced"))
    advancedButton.grid(row=5, column=0, pady=8)

    exitButton = tk.Button(root, text="Exit", font=("Trebuchet MS", 15, "bold"), command=root.destroy)
    exitButton.grid(row=6, column=0, pady=10)

def startQuiz(selectedLevel):
    global difficultyLevel, score, questionCount, attempts
    difficultyLevel = selectedLevel
    score = 0
    questionCount = 1
    attempts = 1
    showQuestion()

def showQuestion():
    global currentAnswer
    questionText, currentAnswer = generateQuestion(difficultyLevel)
    displayProblem(questionText, questionCount, score)

def displayProblem(questionText, questionNumber, currentScore):
    global checkAnswerLabel, answerEntry, submitButton
    clearScreen()

    questionHeader = tk.Label(root, text="Arithmetic Maths Quiz", font=("Trebuchet MS", 22, "bold"), fg="#123456")
    questionHeader.grid(row=0, column=0, pady=(15, 5))

    progressText = "Question " + str(questionNumber) + " of " + str(totalQuestions)
    progressLabel = tk.Label(root, text=progressText, font=("Trebuchet MS", 12, "italic"), fg="#555555")
    progressLabel.grid(row=1, column=0, pady=2)

    questionLabel = tk.Label(root, text=questionText, font=("Trebuchet MS", 20))
    questionLabel.grid(row=2, column=0, padx=5, pady=8)

    givenAnswer.set("")
    answerEntry = tk.Entry(root, textvariable=givenAnswer, font=("Trebuchet MS", 20))
    answerEntry.grid(row=3, column=0, pady=10)
    answerEntry.bind("<Return>", lambda event: handleSubmit())
    answerEntry.focus()

    submitButton = tk.Button(root, text="Submit", font=("Trebuchet MS", 15), command=handleSubmit)
    submitButton.grid(row=4, column=0, pady=5)

    checkAnswerText.set("")
    pointsText.set("")
    totalScoreText.set("Current Score: " + str(currentScore) + " pts")

    checkAnswerLabel = tk.Label(root, textvariable=checkAnswerText, font=("Trebuchet MS", 12, "bold"),
                                wraplength=400, justify="center")
    checkAnswerLabel.grid(row=5, column=0, pady=(4, 2))

    pointsLabel = tk.Label(root, textvariable=pointsText, font=("Trebuchet MS", 11, "italic"), fg="#444444",
                           wraplength=400, justify="center")
    pointsLabel.grid(row=6, column=0, pady=(0, 2))

    totalScoreLabel = tk.Label(root, textvariable=totalScoreText, font=("Trebuchet MS", 11, "bold"), fg="#123456")
    totalScoreLabel.grid(row=7, column=0, pady=(0, 5))

    backButton = tk.Button(root, text="Back to Menu", font=("Trebuchet MS", 11), command=displayMenu)
    backButton.grid(row=8, column=0, pady=(2, 5))


def isCorrect(userAnswer, correctAnswer, attemptNumber):
    if userAnswer == correctAnswer:
        checkAnswerText.set("Your answer is correct!")
        checkAnswerLabel.config(fg="#52a447")
        return True

    if attemptNumber == 1:
        checkAnswerText.set("Incorrect, you have 1 more chance!")
    else:
        checkAnswerText.set("Your answer is incorrect.")
    checkAnswerLabel.config(fg="#e50e0e")
    return False


def lockAndAdvance(delay):
    global locked, pendingJob
    locked = True
    answerEntry.config(state="disabled")
    submitButton.config(state="disabled")
    pendingJob = root.after(delay, nextQuestion)


def handleSubmit():
    global attempts, score

    if locked:
        return

    try:
        userAnswer = int(givenAnswer.get())
    except ValueError:
        checkAnswerText.set("Please enter a valid number.")
        checkAnswerLabel.config(fg="#d97706")
        pointsText.set("")
        return

    if isCorrect(userAnswer, currentAnswer, attempts):
        if attempts == 1:
            points = 10
        else:
            points = 5
        score = score + points
        pointsText.set("+" + str(points) + " points")
        totalScoreText.set("Current Score: " + str(score) + " pts")
        lockAndAdvance(1200)
    elif attempts == 1:
        attempts = 2
        givenAnswer.set("")
    else:
        pointsText.set("0 points. The answer was " + str(currentAnswer) + ".")
        lockAndAdvance(1500)


def nextQuestion():
    global questionCount, attempts, locked, pendingJob
    locked = False
    pendingJob = None
    questionCount = questionCount + 1
    attempts = 1

    if questionCount > totalQuestions:
        displayResults(score)
    else:
        showQuestion()


def getRank(finalScore):
    if finalScore >= 90:
        return "A+", "Excellent, you got an A+! :D"
    elif finalScore >= 80:
        return "A", "Great job, you got an A! :D"
    elif finalScore >= 70:
        return "B", "Good effort, you got a B. :)"
    elif finalScore >= 60:
        return "C", "Not bad, you got a C. :)"
    elif finalScore >= 50:
        return "D", "You passed with a D. :)"
    else:
        return "F", "Better luck next time.. :("


def displayResults(finalScore):
    clearScreen()
    rank, message = getRank(finalScore)

    resHeader = tk.Label(root, text="Quiz Completed!", font=("Trebuchet MS", 24, "bold"), fg="#123456")
    resHeader.grid(row=0, column=0, pady=(20, 10))

    scoreText = "Final Score: " + str(finalScore) + " / 100"
    scoreLabel = tk.Label(root, text=scoreText, font=("Trebuchet MS", 16, "bold"))
    scoreLabel.grid(row=1, column=0, pady=8)

    rankText = "Ranking: " + rank
    rankLabel = tk.Label(root, text=rankText, font=("Trebuchet MS", 16, "bold"), fg="#52a447")
    rankLabel.grid(row=2, column=0, pady=8)

    messageLabel = tk.Label(root, text=message, font=("Trebuchet MS", 14), fg="#333333",
                            wraplength=400, justify="center")
    messageLabel.grid(row=3, column=0, pady=8)

    playAgainButton = tk.Button(root, text="Try Again?", font=("Trebuchet MS", 14, "bold"), command=displayMenu)
    playAgainButton.grid(row=4, column=0, pady=12)

    exitButton = tk.Button(root, text="Exit", font=("Trebuchet MS", 14, "bold"), command=root.destroy)
    exitButton.grid(row=5, column=0, pady=5)


displayMenu()
root.mainloop()