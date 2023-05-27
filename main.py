# Project Title: Flight Tracker Informative Chatbot
# Made by: Carl Lyon
# Subject: Project

# Import required libraries
from tkinter import *
from tkinter import scrolledtext
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy.linalg import norm
import datetime

# Assign a list of sentences which will be added to the answers text file in order to be concatenated with the retrieved flight data as to form whole answer sentences
flight_data_fields = ['The icao24 of the plane is: ', 'The call sign of the plane is: ', 'The origin country of the plane is: ', 'The time position of the plane is: ', 'The last contact made with the plane was: ', 'The longitude of the plane is: ', 'The latitude of the plane is: ', 'THe baro altitude of the plane is: ', 'Is the plane on the ground: ', 'The velocity of the plane is: ', 'The geo altitude of the plane is: ', 'The squawk of the plane is: ', 'SPI: ']

# Define an empty flight questions list
flightQuestions = []

# Define an empty flight answers list
flightAnswers = []

def cosineSimilarity(questionsFile, answersFile):
    """Returns the similarity between the questions file and the answers file """
    questionsFile = np.array(questionsFile)
    answersFile = np.array(answersFile)
    return np.dot(questionsFile, answersFile) / (norm(questionsFile) * norm(answersFile))


def clearTerminal():
    """Clears all the text in the terminal window"""
    T.configure(state=NORMAL)
    T.delete("1.0", "end")
    T.configure(state=DISABLED)

def cleanAnswersFile():
    """The flight answers text file is cleared"""
    with open("f_answers.txt", 'w') as fileClean:
        pass

def getPlaneData():
    """The specified plane data is requested and retrieved, the data is then added to the flight answers
       text file in order with the list of answers sentences concatenated beforehand to form a whole answer
       sentence, per answer traversed in the for loop. If the plane data was not retrieved, print that the aircraft
       is currently not flying in the output terminal"""
    data = requests.get("https://opensky-network.org/api/states/all?icao24=" + hexCode.get().strip()).json()
    if data["states"] != None:
        a = open("f_answers.txt", 'w')
        for i in range(0, 13):
            a.write(str(flight_data_fields[i] + str(data["states"][0][i]).strip()) + "\n")
    else:
        T.configure(state=NORMAL)
        T.insert(END, "The specifed aircraft is currently not flying")
        T.configure(state=DISABLED)

def submitHexCode():
    """The hex code is obtained from the input text box, and is then validated to ensure that it is not empty.
       If the hex code is empty, the hex code entry box's background colour will change to red and will be disabled (non-editable).
       Otherwise, if the hex code is valid, the hex code entry box's background colour will change to red and the hex code inputted,
       will be displayed to the output terminal"""
    code = hexCode.get().strip()
    if code == "":
        hexCodeEntry.configure(background="red")
        questionEntry.configure(state=DISABLED)

    else:
        hexCodeEntry.configure(background="green")
        T.configure(state=NORMAL)
        T.insert(END, "HEX Code: " + code + "\n--------------------------------\n\n")
        T.configure(state=DISABLED)
        questionEntry.configure(state=NORMAL)

def addToLog(question):
    """The current data is obtained and the log text file is opened and is then appended to by adding the current date along with the question asked.
    The log file is then closed."""
    currentDate = datetime.datetime.now()
    log = open("f_log.txt", 'a')
    log.write('Log Entry on Date: ' + str(currentDate) + '\n\n' + 'Question: ' + question + '\n\n' + '===============================================' + '\n\n')
    log.close()

def matchQuestionWithAnswer():
    """The answers text file is opened and read each answer which is then added to the flight answers list. The question inputted by the user is then vectorized,
    and an if statement to check if there are any numbers which are not zero in the vectorized inputted question matrix.
    If true, then the cosine similarity of the vectorized question is obtained and checks if the cosine similarity of the question is greater than 0.
    If true, then the value (matched answer) is assigned to the matchedAnswer variable. When the answer has been found,
    display the matched answer to the output terminal. Otherwise, output that no answers were founded and ask the user to enter another question."""
    with open("f_answers.txt") as f:
        flightAnswers = f.readlines()
    flightQuestionVector = tfidf_vectorizer.transform([questionEntry.get()])

    if flightQuestionVector.toarray()[0].any():
        for value in range(tfidf_matrix.shape[0]):
            flightQuestionSimilarity = cosineSimilarity(tfidf_matrix.toarray()[value], flightQuestionVector.toarray()[0])
            if flightQuestionSimilarity > 0:
                matchedAnswer = value
        T.configure(state=NORMAL)
        T.insert(END, flightAnswers[matchedAnswer])
        T.configure(state=DISABLED)
    else:
        T.configure(state=NORMAL)
        T.insert(END, "No matched answers found... Please try ask another question.")
        T.configure(state=DISABLED)

def submitQuestion():
    """The output terminal is cleared and the inputted question is retrieved and is then validated to check if it is empty or not. If the question is empty, the background of the question input box is red.
    If the user typed 'quit' in the question input box, the application will exit. otherwise the question input text box background is set to green, the answers file is cleared, the updated plane data is retrieved,
    the question entry is added to a log file and then the process of matching the question with the closest answer from the answer text file is executed"""
    clearTerminal()
    if questionEntry.get() == "":
        questionEntry.configure(background="red")
    elif questionEntry.get() == "quit":
        exit()
    else:
        questionEntry.configure(background="green")
        cleanAnswersFile()
        getPlaneData()
        addToLog(questionEntry.get())
        matchQuestionWithAnswer()

# Open the flight questions text file and add each question to the flight questions list
with open("f_questions.txt") as f:
    flightQuestions = f.readlines()

# Declare the TFIDF vectorizer with a filter for english stop words
tfidf_vectorizer = TfidfVectorizer(stop_words="english")

# Declare the TFIDF matrix which processes the flight questions
tfidf_matrix = tfidf_vectorizer.fit_transform(flightQuestions)

# Reference the tkinter 'tk()' function as variable 'window'
window = Tk()

# Assign the icon of the program
# window.iconbitmap(r"flightappicon.ico")

# Set the window title to 'Flight Tracker Informative Chatbot'
window.title("Flight Tracker Informative Chatbot")

# Lock the size of the GUI
window.resizable(width=False, height=False)

# Set the size of the window to '1000x750'
window.geometry('1000x750')

# Set a custom background colour to the GUI
window.configure(bg="#19376D")

# String container for the hex code to be used in the tkinter entry input box
hexCode = StringVar()

# String container for the question to be used in the tkinter entry input box
question = StringVar()

# Set of properties which define the welcome label which displays "Flight Tracker Informative Chatbot"
welcome = Label(window, text="Flight Tracker Informative Chatbot", font="Arial 20 bold")
welcome.place(relx=0.5, rely=0.125, anchor=CENTER)
welcome.configure(bg="#19376D")
welcome.configure(fg="white")

# Set of properties which make up a string made up of many dashes
sep1 = Label(window, text="-----------------------------------------------------------------------------------------------------------", font="Arial 12 italic")
sep1.place(relx=0.5, rely=0.165, anchor=CENTER)
sep1.configure(bg="#19376D")
sep1.configure(fg="white")

# Set of label properties to show the text "Instructions"
instructions = Label(window, text="Instructions", font="Arial 14 underline")
instructions.place(relx=0.5, rely=0.2, anchor=CENTER)
instructions.configure(bg="#19376D")
instructions.configure(fg="white")

# Set of label properties to show the first instruction step
s1 = Label(window, text="1: Input the flight hex code", font="Arial 12 italic")
s1.place(relx=0.5, rely=0.275, anchor=CENTER)
s1.configure(bg="#19376D")
s1.configure(fg="white")

# Set of label properties to show the second instruction step
s2 = Label(window, text="2: Input a question", font="Arial 12 italic")
s2.place(relx=0.5, rely=0.375, anchor=CENTER)
s2.configure(bg="#19376D")
s2.configure(fg="white")

# Set of label properties to show the third instruction step
s3 = Label(window, text="3: Output will be shown in the terminal", font="Arial 12 italic")
s3.place(relx=0.5, rely=0.475, anchor=CENTER)
s3.configure(bg="#19376D")
s3.configure(fg="white")

# Set of properties which make up a string made up of many dashes
sep2 = Label(window, text="-----------------------------------------------------------------------------------------------------------", font="Arial 12 italic")
sep2.place(relx=0.5, rely=0.525, anchor=CENTER)
sep2.configure(bg="#19376D")
sep2.configure(fg="white")

# Set of properties which display the '--- Input flight hex code ---' label
in1 = Label(window, text="--- Input flight hex code ---", font="Arial 10 bold")
in1.place(relx=0.5, rely=0.575, anchor=CENTER)
in1.configure(bg="#19376D")
in1.configure(fg="white")

# Properties which make up the hex code input text box
hexCodeEntry = Entry(window, textvariable=hexCode, font = ('calibre',10,'bold'), width = 50)
hexCodeEntry.place(relx=0.5, rely=0.6, anchor=CENTER)

# Properties which make up the submit hex code button
sub_btn_hex = Button(window, text = "Submit Hex Code", command = submitHexCode)
sub_btn_hex.place(relx=0.5, rely=0.6375, anchor=CENTER)

# Properties which make up the question input text box
questionEntry = Entry(window, textvariable=question, font = ('calibre',10,'bold'), width = 50)
questionEntry.place(relx=0.5, rely=0.705, anchor=CENTER)
questionEntry.configure(state=DISABLED)

# Properties which make up the question submit button
sub_btn_question = Button(window, text = "Submit Question", command = submitQuestion)
sub_btn_question.place(relx=0.5, rely=0.75, anchor=CENTER)

# Set of properties which define the label which display '--- Input Question ---'
in2 = Label(window, text="--- Input question ---", font="Arial 10 bold")
in2.place(relx=0.5, rely=0.675, anchor=CENTER)
in2.configure(bg="#19376D")
in2.configure(fg="white")

# Set of properties which define the label which displays '--- Output Terminal ---'
in3 = Label(window, text="--- Output Terminal ---", font="Arial 10 bold")
in3.place(relx=0.5, rely=0.775, anchor=CENTER)
in3.configure(bg="#19376D")
in3.configure(fg="white")

# Set of properties which define the label which displays 'Clear Terminal'
btn_clear = Button(window, text = "Clear Terminal", command = clearTerminal)
btn_clear.place(relx=0.5, rely=0.95, anchor=CENTER)

# Set of properties which define the scrolled text area which will be used as the terminal window
T = scrolledtext.ScrolledText(window, height = 5, width = 50)
T.place(relx=0.5, rely=0.80, anchor='n')
T.configure(state=DISABLED)

# Set of properties which define the credits label in the tkinter GUI
credits = Label(window, text="Made by Carl Lyon", font="Arial 12 italic")
credits.place(relx=0.1, rely=0.975, anchor=CENTER)
credits.configure(bg="#19376D")
credits.configure(fg="white")

# Loop the GUI screen
window.mainloop()