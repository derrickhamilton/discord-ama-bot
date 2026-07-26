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
 
def handleQuestionSubmission(authorString, questionContentString):
    questionsData = {}

    # Define a dictionary structure using the questions.json file created by AMA-bot
    with open("questions.json", "r") as questionsFile:
        questionsData = json.load(questionsFile)

    # Get today's date in yyyy-mm-dd format
    today = date.today().isoformat()

    newQuestionData = {"author": authorString, "dateSubmitted": today, "questionContent": questionContentString}
    questionsData["questions"].append(newQuestionData)

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
        print(f"Submission from user {interaction.user.display_name}: {self.msg_content.value}")

        handleQuestionSubmission(interaction.user.display_name, self.msg_content.value)

        await interaction.response.send_message(f"{interaction.user.mention} - Thank you for submitting a question!")

class LaunchQuestionSubmissionFormView(discord.ui.View):

    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary, custom_id="open_form_button")
    async def open_form(self, interaction: discord.Interation, button: discord.ui.Button):
        await interaction.response.send_modal(QuestionSubmissionForm())
