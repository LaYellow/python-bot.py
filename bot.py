import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import has_permissions
import asyncio
from itertools import cycle
import time
import youtube_dl
import random
import re
import aiohttp
from datetime import timedelta
import traceback
import os
from random import choice, randint


status = ['Bot under snsbdevelopement', 'please be patibsjsbence']


bot = commands.Bot(command_prefix=".", status=discord.Status.dnd, activity=discord.Game('Sleeping'), self_bot=True)

@bot.event
async def on_ready():
	print('K ass')


bot.run("NTk3NTk3ODE0MjMwNDgyOTYz.XSKaYQ.YcYSKb55gqMq12lwGCfr2WXTGo4",bot=False)
