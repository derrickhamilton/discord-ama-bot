#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-28-2026
# Purpose: Defines methods to handle data from questions.db
#-----------------------------------------------------------------

import json
import sqlite3
import aiosqlite
from datetime import date

DB_FILE_NAME = "questions.db"

async def initializeDb():
    async with aiosqlite.connect(DB_FILE_NAME) as db:
        try:
            await db.execute("""
                PRAGMA foreign_keys = ON;
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS Servers (
                    id VARCHAR(255) PRIMARY KEY
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS Questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id VARCHAR(255),
                    author VARCHAR(255) NOT NULL,
                    question VARCHAR(280) NOT NULL,
                    asked BOOL NOT NULL,
                    FOREIGN KEY (server_id) REFERENCES Servers(id)
                )
            """)

            await db.commit()

        except sqlite3.Error as error:
            print(f"SQLite error occurred: {error}")
            await db.rollback()

async def submitNewServerToDb(serverId):
    async with aiosqlite.connect(DB_FILE_NAME) as db:
        try:
            # Insert new server ID into Servers table
            await db.execute(
                "INSERT INTO Servers (id) VALUES (?)",
                (serverId,)
            )

            # Commit to save changes
            await db.commit()

        except sqlite3.Error as error:
            print(f"SQLite error occurred: {error}")
            await db.rollback()
            raise

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