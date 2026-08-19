#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-28-2026
# Purpose: Defines methods to handle data from questions.json
#-----------------------------------------------------------------

import json
from datetime import date

def submitNewQuestionToJson(authorString, questionContentString, serverNameString):
    questionsData = {}

    # Define a dictionary structure using the questions.json file created by AMA-bot
    with open("questions.json", "r") as questionsFile:
        questionsData = json.load(questionsFile)

    # Get today's date in yyyy-mm-dd format
    today = date.today().isoformat()

    for index, server in enumerate(questionsData.get("servers")):
        serverNameValue = server.get("server-name", "Unknown")
        print(f"Compare to value: {serverNameString} retrieved value:{serverNameValue}")
        if serverNameString == serverNameValue:
            print("Found server! Name: " + serverNameString)
            newQuestionData = {"author": authorString, "dateSubmitted": today, "questionContent": questionContentString}
            questionsData["servers"][index]["questions"].append(newQuestionData)
            break;

    with open("questions.json", "w") as newQuestionsFile:
        json.dump(questionsData, newQuestionsFile, indent=4)

def retrieveQuestionFromJson(serverNameString):
    questionsData = {}
    questionReturnStr = ""

    # Define a dictionary structure using the questions.json file created by AMA-bot
    with open("questions.json", "r") as questionsFile:
        questionsData = json.load(questionsFile)

    for index, server in enumerate(questionsData.get("servers")):
        serverNameValue = server.get("server-name", "Unknown")
        if serverNameString == serverNameValue:

            # If questions list is empty, simply return to avoid list pop error
            if len(questionsData["servers"][index]["questions"]) == 0:
                return questionReturnStr

            # Grab the first question from the questions list then append it to the askedQuestions list
            selectedQuestionData = questionsData["servers"][index]["questions"].pop(0)
            questionReturnStr = selectedQuestionData["questionContent"]
            questionsData["servers"][index]["askedQuestions"].append(selectedQuestionData)

    with open("questions.json", "w") as newQuestionsFile:
        json.dump(questionsData, newQuestionsFile, indent=4)


    return questionReturnStr