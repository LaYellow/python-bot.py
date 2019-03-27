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

my_token = 'NTQyNTAyNjIzNjY4OTk0MDY5.DzvCIw.JoOolByOgGw3OqT4pnOMf5Xc5E8'

client = commands.Bot(command_prefix = '/')

client.remove_command('help')
status = ['with /help | commands', 'with LaYellow#9207', ]

players = {}


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name =current_status, type = 1))
        await asyncio.sleep(5)

@client.event
async def on_ready():
    print('The bot is online and is connected to discord')

@client.event
async def on_message(message):
    
    await client.process_commands(message)
    if message.content.startswith('/help'):
        userID = message.author.id
        await client.send_message(message.channel, '<@%s> ***Check DM For Information*** :mailbox_with_mail: ' % (userID))

@client.command(pass_context =True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(Colour = discord.Colour.orange())
    embed.set_author(name = 'Help Commands')
    embed.add_field(name ='/say', value ='Returns what the user says.', inline=False)
    embed.add_field(name ='/purge', value ='Only administrator can use this command.', inline=False)
    embed.add_field(name ='/join', value ='Let the bot connect to the current voice chat you are in.', inline=False)
    embed.add_field(name ='/play', value ='Play a video/music from youtube URL.', inline=False)
    embed.add_field(name ='/stop', value ='Pause  the current playing video/msuic.', inline=False)
    embed.add_field(name ='/resume', value ='Resume the current playing video/music.', inline=False)
    embed.add_field(name ='/leave', value ='Leave the voice chat you are in.', inline=False)
    embed.add_field(name ='/donate', value ='Give the wallet link to donate me.', inline=False)
    embed.add_field(name ='/profile', value ='Show a user profile using /profile @LaYellow#9207.', inline=False)
    embed.add_field(name ='/render', value ='Show a Growtopia world.', inline=False)
    embed.add_field(name ='/howgay', value ='R8 Gay machine.', inline=False)
    embed.add_field(name ='/howretard', value ='R8 Retard machine.', inline=False)
    embed.add_field(name ='/serverid', value ='Send ID of the current server you are in.', inline=False)
    embed.add_field(name ='/ping', value ='Send speed of the current bot network.', inline=False)
    embed.add_field(name ='/dice', value ='Play a dice game when youre bored number between 1-6.', inline=False)
    embed.add_field(name ='/invite', value ='Invite the bot to your server.', inline=False)

    await client.send_message(author, embed=embed)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def purge(ctx, amount = 10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' **messages were deleted so ya!** ')


@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    embed = discord.Embed(
        title = 'Voice channel',
        description = 'commands for the voice channel.',
        colour = discord.Colour.blue()
    )

    embed.add_field(name = '/play', value = 'play youtube audio with url', inline = False)
    embed.add_field(name = '/pause', value = 'pauses audio', inline = False)
    embed.add_field(name = '/stop', value = 'resumes audio', inline = False)
    embed.add_field(name = '/leave', value = 'leave voice channel', inline = False)

    await client.say(embed=embed)
    await client.join_voice_channel(channel)


@client.command(pass_context = True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(pass_context = True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    """Kick A User from server"""
    await client.kick(userName)
    await client.say("__**Successfully User Has Been Kicked!**__")

@client.command(pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, userName: discord.User):
    """Ban A User from server"""
    await client.ban(userName)
    await client.say("__**Successfully User Has Been Banned!**__")

@client.command(pass_context = True)
@commands.has_permissions(administrator_members=True)
async def unban(ctx, userName: discord.User):
    """Unban A User from server"""
    await client.kick(userName)
    await client.say("__**Successfully User Has Been Unbanned**__")

@client.command(pass_context = True)
async def say(ctx, *args):
    mesg = ' '.join(args)
    await asyncio.sleep(0.4)
    await client.delete_message(ctx.message)
    return await client.say(mesg)


@client.command(pass_context=True)
async def profile(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.add_field(name='Dont Abuse',value = 'Dont Abuse This Command Because This Command is not stable', inline= False)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)
    
@client.command()
async def donate():
  await client.say('The Wallet link of Bitcoin:point_down:')
  await client.say('```1LhJF2fsD8LksH77oWULJCkEFhY7K8JM3b```')

@client.command()
async def render(type):
	await client.say('https://growtopiagame.com/worlds/'f'{type}.png')

@client.command()
async def howgay( *args):
	
    g = random.randint(1,100)
    output = ''
    if str(args) == '()':
        args = 'You'
        areis = 'are'
    else:
        areis = 'is'
    for word in args:
        output += word
    await client.say(':gay_pride_flag: **{} {} {}% gay ** '.format(output, areis ,g))
    
@client.command()
async def howretard( *args):
	
    g = random.randint(1,100)
    output = ''
    if str(args) == '()':
        args = 'You'
        areis = 'are'
    else:
        areis = 'is'
    for word in args:
        output += word
    await client.say(':clap: **{} {} {}% retard **'.format(output, areis ,g))
   
@client.command(pass_context=True)
async def avatar(ctx, user: discord.Member):
    embed = discord.Embed(title="{}".format(user.name),description="", color=0x00ff00)
    embed.set_image(url=user.avatar_url)
    await client.say(embed=embed)
    
@client.command()
async def invite():
  	"""Bot Invite"""
  	await client.say('```Please check your DMs```')
  	await client.whisper("Add me with this link {}".format(discord.utils.oauth_url(client.user.id)))
	
@client.command(pass_context=True)
async def ping(ctx):
    t = await client.say('Pong')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await client.edit_message(t, new_content='{}ms'.format(int(ms)))

@client.command(pass_context=True)
async def serverid(ctx):
	  await client.say("```{}```".format(ctx.message.server.id))

@client.command()
async def dice():
	dice = random.choice(['1','2','3','4','5','6'])
	await client.say(dice)
	
@client.command()
async def developer():
	await client.say(```'<@%s>'```)

client.loop.create_task(change_status())
client.run(str(os.environ.get('TOKEN')))
