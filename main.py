#-----------------------------------------------------------------
# Author:  Derrick Hamilton
# Date:    07-23-2026
# Purpose: main.py file for my Discord AMA-bot
#-----------------------------------------------------------------

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
from gtts import gTTS
import os
import asyncio
import sqlite3
from questionSubmissionForm import LaunchQuestionSubmissionFormView
from handleQuestionData import initializeDb, retrieveQuestionDataFromJson, submitNewServerToDb

load_dotenv()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class AmaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members         = True
        intents.voice_states    = True
        intents.guilds          = True

        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f"Hello, I am {self.user.name}. I am ready to ask you anything!")

        await initializeDb()

        # Persist the question submission form button between bot restarts
        self.add_view(LaunchQuestionSubmissionFormView())

bot = AmaBot()

@bot.event
async def on_guild_join(guild):
    print(f"Joined new server: {guild.name}")

    try:
        # Submit new server to stored server data
        await submitNewServerToDb(guild.id)

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

    except sqlite3.Error:
        # Find first chat channel where bot has permission to send a message
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f"Whoops! Unable to add {guild.name} into database.")

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
# Upon usage, AMA-bot will attempt to join the voice channel the user requesting is joined
# to use TTS to ask a question
# Will not do anything if the user is not currently in a voice channel
@bot.command(name="ama")
async def ama(ctx):
    # Attempt to retrieve a question from the json data
    question = retrieveQuestionDataFromJson(ctx.guild.name)

    if not question:
        await ctx.send(f"{ctx.author.mention} - No question found! Consider submitting a question using the submit-question command.")
    else:
        if not ctx.author.voice:
            await ctx.send(f"{ctx.author.mention} - {question["questionContent"]}")
        else:
            voiceChannel = ctx.author.voice.channel

            # Create the questionStr to be converted to audio saying who submitted it and the question content
            questionStr = f"{question["author"]} asked - {question["questionContent"]}"

            # Convert questionStr to an MP3 file using gTTS
            ttsAudio = gTTS(text=questionStr, lang="en")
            filename = "tts_question_audio.mp3"
            ttsAudio.save(filename)

            # Join voice channel
            vc = await voiceChannel.connect()

            # Play audio using ffmpeg
            vc.play(discord.FFmpegPCMAudio(source=filename))

            # Wait for audio clip to finish
            while vc.is_playing():
                await asyncio.sleep(1)

            # Disconnect and cleanup
            await vc.disconnect()
            if os.path.exists(filename):
                os.remove(filename)

            # Still output question to text channel after disconnecting from voice
            await ctx.send(f"{ctx.author.mention} - {question["questionContent"]}")

# Command: !submit-question
# Sends a message containing a button to launch the QuestionSubmissionForm modal 
# using the LaunchQuestionSubmissionFormView class
@bot.command(name="submit-question")
async def submit(ctx):
    # Flag to check if the author of a message in the pinned messages list is AMA-bot
    foundAmaBotMessage = False

    # Get all the pinned messages from the current text channel
    # await ctx.channel.pins() is deprecated
    async for message in ctx.channel.pins():
        if message.author == bot.user:
            foundAmaBotMessage = True

    # Create an embed to hold a brief instruction message with the submission form launcher
    question_embed = discord.Embed(
        title="Submit a question to AMA-bot! ❓",
        description="To submit your question, click the button below to fill out the question submission form.",
        color=discord.Color.blue()
    )
    
    questionFormMessage = await ctx.send(embed=question_embed, view=LaunchQuestionSubmissionFormView())

    # If AMA-bot's message was not found in the pinned messages list, pin it
    if not foundAmaBotMessage:
        await questionFormMessage.pin()

    
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("DISCORD_TOKEN is missing from the environment variables!")

    # Run the bot
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)