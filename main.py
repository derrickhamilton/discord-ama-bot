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

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Hello, I am {bot.user.name}. I am ready to ask you anything!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Intending to receive AMA questions through DMs to AMA-bot
    # !submit command must be used to 'hopefully' mitigate junk messages
    if message.guild is None:
        print(f"Received DM from {message.author}: {message.content}")
        await message.author.send("I am but a mere robot. I respectfully ask that you only utilize the !submit command here")

    # Needed to ensure bot can still process commands
    await bot.process_commands(message)

# Command: !ama
# Upon usage, user will receive a question from the bot
@bot.command()
async def ama(ctx):
    await ctx.send(f"{ctx.author.mention} - Is Rascal a bratto or a catto?")

# Command: !submit
# Upon usage in DM with AMA-bot, will save the question
# If used in a server, will prompt the user to send a DM to the bot
@bot.command()
async def submit(ctx, *, msg):
    if ctx.guild is None:
        print(f"Received command from {ctx.author}: {msg}")
        await ctx.author.send("Thank you for submitting your question. I will remember to ask this in the future!")
        return

    await ctx.send(f"{ctx.author.mention} - Thank you for showing interest in submitting a question to be asked. \
                   Send me a DM using !submit followed by your message content so I can save it secretly! 🤫")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)