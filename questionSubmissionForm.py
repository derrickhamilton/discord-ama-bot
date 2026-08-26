#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-25-2026
# Purpose: Defines classes to create a question submission from
#          for my Discord AMA-bot
#-----------------------------------------------------------------

import discord
from handleQuestionData import submitNewQuestionToJson

questionFormTitleString = "Submit a question!"

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
        submitNewQuestionToJson(interaction.user.display_name, self.msg_content.value, interaction.guild.name)

        await interaction.response.send_message(f"{interaction.user.mention} - Thank you for submitting a question!")

class LaunchQuestionSubmissionFormView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
            label="Submit",
            style=discord.ButtonStyle.primary,
            custom_id="open_question_form_button"
    )
    
    async def open_form(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(QuestionSubmissionForm())
