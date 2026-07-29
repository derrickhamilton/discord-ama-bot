#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-25-2026
# Purpose: Defines classes to create a question submission from
#          for my Discord AMA-bot
#-----------------------------------------------------------------

import discord
import json
from datetime import date

questionFormTitleString = "Submit a question!"
 
def handleQuestionSubmission(authorString, questionContentString, serverNameString):
    questionsData = {}

    # Define a dictionary structure using the questions.json file created by AMA-bot
    with open("questions.json", "r") as questionsFile:
        questionsData = json.load(questionsFile)

    # Get today's date in yyyy-mm-dd format
    today = date.today().isoformat()

    i = 0
    for server in questionsData.get("servers"):
        serverNameValue = server.get("server-name", "Unknown")
        print(f"Compare to value: {serverNameString} retrieved value:{serverNameValue}")
        if serverNameString == serverNameValue:
            print("Found server! Name: " + serverNameString)
            newQuestionData = {"author": authorString, "dateSubmitted": today, "questionContent": questionContentString, "asked": False}
            questionsData["servers"][i]["questions"].append(newQuestionData)
            break;
        i += 1

    with open("questions.json", "w") as newQuestionsFile:
        json.dump(questionsData, newQuestionsFile, indent=4)

class QuestionSubmissionForm(discord.ui.Modal, title=questionFormTitleString):

    msg_content = discord.ui.TextInput(
        label="Question Box",
        placeholder="Type your question here...",
        max_length=400
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Need to handle the text submitted through the form
        print(f"Submission from user {interaction.user.display_name}: {self.msg_content.value}\nServer: {interaction.guild}")

        assert interaction.guild is not None
        handleQuestionSubmission(interaction.user.display_name, self.msg_content.value, interaction.guild.name)

        await interaction.response.send_message(f"{interaction.user.mention} - Thank you for submitting a question!")

class LaunchQuestionSubmissionFormView(discord.ui.View):

    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary, custom_id="open_form_button")
    async def open_form(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(QuestionSubmissionForm())
