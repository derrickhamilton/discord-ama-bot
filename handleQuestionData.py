#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-28-2026
# Purpose: Defines methods to handle data from questions.json
#-----------------------------------------------------------------

import json
from datetime import date

def submitNewServerToJson(serverNameString):
    questionsData = {}
    
    # Define a dictionary structure using the questions.json file created by AMA-bot
    with open("questions.json", "r") as questionsFile:
        questionsData = json.load(questionsFile)

    # Iterate through the servers in questionsData to see if server already exists
    for server in questionsData.get("servers"):
        serverNameValue = server.get("serverName", "Unknown")
        if serverNameString == serverNameValue:
            print("Server already exists! Name: " + serverNameString)
            return

    # Submit new server info to questionsData
    newServerData = {"serverName": serverNameString, "questions": [], "askedQuestions": []}
    questionsData["servers"].append(newServerData)

    with open("questions.json", "w") as newQuestionsFile:
        json.dump(questionsData, newQuestionsFile, indent=4)

def submitNewQuestionToJson(authorString, questionContentString, serverNameString):
    questionsData = {}

    # Define a dictionary structure using the questions.json file created by AMA-bot
    with open("questions.json", "r") as questionsFile:
        questionsData = json.load(questionsFile)

    # Get today's date in yyyy-mm-dd format
    today = date.today().isoformat()

    for index, server in enumerate(questionsData.get("servers")):
        serverNameValue = server.get("serverName", "Unknown")
        print(f"Compare to value: {serverNameString} retrieved value:{serverNameValue}")
        if serverNameString == serverNameValue:
            print("Found server! Name: " + serverNameString)
            newQuestionData = {"author": authorString, "dateSubmitted": today, "questionContent": questionContentString}
            questionsData["servers"][index]["questions"].append(newQuestionData)
            break;

    with open("questions.json", "w") as newQuestionsFile:
        json.dump(questionsData, newQuestionsFile, indent=4)

def retrieveQuestionDataFromJson(serverNameString):
    allQuestionsData = {}
    questionReturn = {}

    # Define a dictionary structure using the questions.json file created by AMA-bot
    with open("questions.json", "r") as questionsFile:
        allQuestionsData = json.load(questionsFile)

    for index, server in enumerate(allQuestionsData.get("servers")):
        serverNameValue = server.get("serverName", "Unknown")
        if serverNameString == serverNameValue:

            # If questions list is empty, simply return to avoid list pop error
            if len(allQuestionsData["servers"][index]["questions"]) == 0:
                return questionReturn

            # Grab the first question from the questions list then append it to the askedQuestions list
            questionReturn = allQuestionsData["servers"][index]["questions"].pop(0)
            allQuestionsData["servers"][index]["askedQuestions"].append(questionReturn)

    with open("questions.json", "w") as newQuestionsFile:
        json.dump(allQuestionsData, newQuestionsFile, indent=4)


    return questionReturn