#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-23-2026
# Purpose: main.py file for my Discord AMA-bot
#-----------------------------------------------------------------

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from questionSubmissionForm import LaunchQuestionSubmissionFormView
from handleQuestionData import retrieveQuestionFromJson, submitNewServerToJson

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    assert bot.user is not None
    print(f"Hello, I am {bot.user.name}. I am ready to ask you anything!")

@bot.event
async def on_guild_join(guild):
    print(f"Joined new server: {guild.name}")

    # Submit new server to stored server data
    submitNewServerToJson(guild.name)

    # Find first chat channel where bot has permission to send a message
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            welcomeEmbed = discord.Embed(
                title="AMA-Bot greets you! 👋",
                description=f"Hello, {guild.name}, I am AMA-bot, here to handle all things inquisitive.",
                color=discord.Color.blue()
            )

            await channel.send(embed=welcomeEmbed)

            break;

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None:
        print(f"Received DM from {message.author}: {message.content}")
        await message.author.send("I am but a mere robot. I respectfully ask that you only submit questions by utilizing the submit-question command in a server")

    # Needed to ensure bot can still process commands
    await bot.process_commands(message)

# Command: !ama
# Upon usage, user will receive a question from the bot
@bot.command(name="ama")
async def ama(ctx):
    print(f"Request from author: {ctx.author} on server: {ctx.guild.name} to retrieve question")
    questionStr = retrieveQuestionFromJson(ctx.guild.name)

    if not questionStr:
        await ctx.send(f"{ctx.author.mention} - No question found! Consider submitting a question using the ama command.")
    else:
        await ctx.send(f"{ctx.author.mention} - {questionStr}")

# Command: !submit-question
# Sends a message containing a button to launch the QuestionSubmissionForm modal 
# using the LaunchQuestionSubmissionFormView class
@bot.command(name="submit-question")
@commands.has_permissions(administrator=True)
async def submit(ctx):
    # Create an embed to hold a brief instruction message with the submission form launcher
    question_embed = discord.Embed(
        title="Submit a question to AMA-bot! ❓",
        description="To submit your question, click the button below to fill out the question submission form.",
        color=discord.Color.blue()
    )

    await ctx.send(embed=question_embed, view=LaunchQuestionSubmissionFormView())
    
assert token is not None
bot.run(token, log_handler=handler, log_level=logging.DEBUG)