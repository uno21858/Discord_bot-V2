	#Tanks to meme for solving the join issue
	#aka  worship him

import discord
import random
from discord.ext import commands, tasks
import os
from itertools import cycle
import youtube_dl
import json
import asyncio
import shutil
from discord.utils import get
from os import system






client = commands.Bot(command_prefix = '$')


@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle, activity=discord.Game('The shitty works now'))
	print('Bot is ready.')

	#Tanks to meme for solving the join issue
	#aka  worship him




@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
	responses = ['It is certain.',
				 'It is decidlely so.',
				 'Without a doubt.'
				 'Yes - definitely.'
				 'You may rely on it.',
				 'As I see it, yes.',
				 'Most likely.',
				 'Outloock good.',
				 'Yes',
				 'Signs point to yes.',
				 'Reply hazy, try again.',
				 'Ask again later.',
				 'Better not tell you now.',
				 'Cannot predict now.',
				 'Just owo with it.',
				 'Dont count on it.',
				 'My reply is no.',
				 'My resources say no.',
				 'Yahoo piece of shit.',
				 'Very doubtful.',
				 'shut the fuck up.',
				 'No you']

	await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if(user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
			return

# Musica q pondra el Bot

@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()

	await voice.disconnect()

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		print(f"The bot has connected to {channel}\n")

	await ctx.send(f"Joined{channel}")

@client.command(pass_context=True, aliases=['l', 'lea', 'fuckoff'])
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
		print(f"The bot has left {channel}")
		await ctx.send(f"Left {channel}")
	else:
		print("The bot was told to leave voice channel, but was not in one")
		await ctx.send("Don't think I am in a voice channel")

@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
	global name 

	def check_queue():
		Queue_infile = os.path.isdir("./Queue")
		if Queue_infile is True:
			DIR = os.path.abspath(os.path.realpath("Queue"))
			length = len(os.listdir(DIR))
			still_q = length - 1 
			try:
				first_file = os.listdir(DIR) [0]
			except:
				print("No more queued song(s)\n")
				queues.clear()
				return
			main_location = os.path.dirname(os.path.realpath(__file__))
			song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
			if length != 0:
				print("Song done, playing next queued\n")
				print(f"Songs still in queue: {still_q}")
				song_there = os.path.isfile("song.mp3")
				if song_there:
					os.remove("song.mp3")
				shutil.move(song_path, main_location)
				for file in os.listdir("./"):
					if file.endswith(".mp3"):
						os.rename(file, 'song.mp3')

				voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
				voice.source = discord.PCMVolumeTransformer(voice.source)
				voice.source.volume = 0.07
			else:
				queues.clear()
				return
		else:
			queues.clear()
			print("No songs queued before the ending of the last song\n")


	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
			queues.clear()
			print("Removed old song file")
	
	except PermissionError:
		print("Trying to delete song file, but is being played ")
		await ctx.send("ERROR: Music playing")
		return
	
	Queue_infile = os.path.isdir("./Queue")
	try:
		Queue_folder = "./Queue"
		if Queue_infile is True:
			print("Removed old Queue Folder")
			shutil.rmtree(Queue_folder)
	except:
		print("No old Queue file")



	await ctx.send("Getting everything now you CUNT")

	voice = get(client.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': True,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio', 
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print("Downloading audio now\n")
			ydl.download([url])
	except:
		print("FALLBACK: youtube-dl does nor support this URL, using Spotify (This is normal if Spotify URl)")
		c_path = os.path.dirname(os.path.realpath(__file__))
		system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			name = file
			print(f"Renamed File: {file}\n")
			os.rename(file, "song.mp3")
	
	voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	nname = name.rsplit("-", 2)
	await ctx.send(f"Playing: {nname}")
	print("playing\n")

@client.command(passcontext=True, aliases=['pa', 'pau'])
async def pause(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)
	
	if voice and voice.is_playing():
		print("Music stopped")
		voice.pause()
		await ctx.send("Music stopped")
	else:
		print("Music not playing failed pause")
		await ctx.send("Music not playing failed to stop")

@client.command(passcontext=True, aliases=['r', 're'])
async def resume(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_paused():
		print("Music resumed")
		voice.resume()
		await ctx.send("Your shit is resumed")
	else:
		print("Music is not paused")
		await ctx.send("Music is not paused")

@client.command(passcontext=True, aliases=['st', 'sto'])
async def stop(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	queues.clear()

	if voice and voice.is_playing():
		print("Music stopped")
		voice.stop()
		await ctx.send("No more of that shit")
	else:
		print("no music playing failed to stop")
		await ctx.send("No music playing failed to stop")

queues = {}

@client.command(passcontext=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
	Queue_infile = os.path.isdir("./Queue")
	if Queue_infile is False:
		os.mkdir("Queue")
	DIR = os.path.abspath(os.path.realpath("Queue"))
	q_num = len(os.listdir(DIR))
	q_num += 1 
	add_queue = True
	while add_queue:
		if q_num in queues:
			q_num += 1
		else:
			add_queue = False
			queues[q_num] = q_num

	queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song(q_num).%%(ext)s")

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': True,
		'outtmpl': queue_path,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio', 
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print("Downloading audio now\n")
			ydl.download([url])
		await ctx.send("Adding song " + str(q_num) + " to the queue")

	except:
		print("FALLBACK: youtube-dl does nor support this URL, using Spotify (This is normal if Spotify URl)")
		q_path = os.path.abspath(os.path.realpath("Queue"))
		system(f"spotdl -f song(q_num) -f " + '"' + q_path + '"' + " -s " + url)



	print("Song added to queue\n")

client.run("Add the thing here ")
