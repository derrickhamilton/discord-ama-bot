#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-28-2026
# Purpose: Defines methods to handle data from questions.db
#-----------------------------------------------------------------

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
                    date TEXT,
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

async def submitNewQuestionToDb(authorString, questionContentString, serverId):
    async with aiosqlite.connect(DB_FILE_NAME) as db:
        try:
            # Get today's date in yyyy-mm-dd format
            today = date.today().isoformat()

            # Insert new questions into Questions table with associated serverId
            await db.execute(
                "INSERT INTO Questions (server_id, author, date, question, asked) VALUES (?,?,?,?,?)",
                (serverId, authorString, today, questionContentString, 0)
            )

            # Commit changes to save
            await db.commit()

        except sqlite3.Error as error:
            print(f"SQLite error occurred: {error}")
            await db.rollback()
            raise

async def retrieveQuestionDataFromDb(serverId):
    async with aiosqlite.connect(DB_FILE_NAME) as db:
        try:
            async with db.execute("SELECT * FROM Questions WHERE server_id = ?", (serverId,)) as cursor:
                # Initialize tuple to store the question data
                foundQuestion = tuple()

                # Access rows one by one
                async for row in cursor:
                    # Check if question was asked in the server
                    questionAsked = row[5] # Corresponds to Questions table 'asked' value

                    if not questionAsked:
                        foundQuestion = row
                        break

                # Return regardless of result
                return foundQuestion

        except sqlite3.Error as error:
            print(f"SQLite error occurred: {error}")
            await db.rollback()
            raise

async def updateQuestionAskedValueInDb(questionId):
    async with aiosqlite.connect(DB_FILE_NAME) as db:
        try:
            await db.execute(
                "UPDATE Questions SET asked = ? WHERE id = ?",
                ("TRUE", questionId)
            )

            await db.commit()

        except sqlite3.Error as error:
            print(f"SQLite error occurred: {error}")
            await db.rollback()
            raise