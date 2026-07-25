#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-25-2026
# Purpose: Defines classes to create a question submission from
#          for my Discord AMA-bot
#-----------------------------------------------------------------

import discord

questionFormTitleString = "Submit a question!"

class QuestionSubmissionForm(discord.ui.Modal, title=questionFormTitleString):

    msg_content = discord.ui.TextInput(
        label="Question Box",
        placeholder="Type your question here...",
        max_length=400
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} - Thank you for submitting a question!")

class LaunchQuestionSubmissionFormView(discord.ui.View):

    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary, custom_id="open_form_button")
    async def open_form(self, interaction: discord.Interation, button: discord.ui.Button):
        await interaction.response.send_modal(QuestionSubmissionForm())
