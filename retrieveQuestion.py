#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-28-2026
# Purpose: Method definition to retrieve question from questions.json
#-----------------------------------------------------------------

import random
import json

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