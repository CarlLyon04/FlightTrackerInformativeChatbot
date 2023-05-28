from tkinter import *
from tkinter import scrolledtext
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy.linalg import norm
import datetime
import unittest

flightQuestions = []

flightAnswers = []

with open("f_questions.txt") as f:
    flightQuestions = f.readlines()

tfidf_vectorizer = TfidfVectorizer(stop_words="english")

# Declare the TFIDF matrix which processes the flight questions
tfidf_matrix = tfidf_vectorizer.fit_transform(flightQuestions)


def cosineSimilarity(questionsFile, answersFile):
    """Returns the similarity between the questions file and the answers file """
    questionsFile = np.array(questionsFile)
    answersFile = np.array(answersFile)
    return np.dot(questionsFile, answersFile) / (norm(questionsFile) * norm(answersFile))


class TestSimilarity(unittest.TestCase):
 
    def test_sim(self):
        with open("f_answers.txt") as f:
            flightAnswers = f.readlines()
        flightQuestionVector = tfidf_vectorizer.transform(["What is the callsign?"])

        if flightQuestionVector.toarray()[0].any():
            for value in range(tfidf_matrix.shape[0]):
                flightQuestionSimilarity = cosineSimilarity(tfidf_matrix.toarray()[value], flightQuestionVector.toarray()[0])
                if flightQuestionSimilarity > 0:
                    matchedAnswer = value
                    answer = flightAnswers[matchedAnswer].replace("\n", "")
                    self.assertEqual(answer, "The call sign of the plane is: DLA13T")
 
        
 
if __name__ == '__main__':
    unittest.main()
