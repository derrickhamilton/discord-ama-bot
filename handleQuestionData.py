#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-28-2026
# Purpose: Defines methods to handle data from questions.json
#-----------------------------------------------------------------

import random
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
            newQuestionData = {"author": authorString, "dateSubmitted": today, "questionContent": questionContentString, "asked": False}
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
            questionsArrayLength = len(questionsData["servers"][index]["questions"])
            randomQuestionInt = random.randint(0, questionsArrayLength-1)
            questionReturnStr = questionsData["servers"][index]["questions"][randomQuestionInt]["questionContent"]


    return questionReturnStr