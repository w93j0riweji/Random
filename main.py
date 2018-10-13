import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import asyncio
import random
from datetime import datetime
from itertools import cycle

#https://pastebin.com/JMVYJpGY -reminder

Client = discord.Client()
client = commands.Bot(command_prefix = "w!")
client.remove_command('help')
status = ['Work in progress :/', 'Prefix: w!', 'Made by Wrong#4794']

async def change_status():
  await client.wait_until_ready()
  msgs = cycle(status)

  while not client.is_closed:
    current_status = next(msgs)
    await client.change_presence(game=discord.Game(name=current_status))
    await asyncio.sleep(10)

@client.event
async def on_ready():
    print("WrongBot is at your service!")
    print(client.user)

@client.event 
async def on_message(message):
  if message.content.startswith('w!reverse') == True:
        await client.send_message(message.channel, message.content[:8:-1])

  if message.content.startswith('w!search'):
        await client.send_typing(message.channel)
        args = message.content.split(" ")
        combargs = (" ".join(args[1:]))
        formatted = combargs.replace(" ", "+")
        em = discord.Embed(title=  (" ".join(args[1:])), url='https://www.google.com/search?source=hp&ei=ojeYW6TEGoz45gKXyI3IBw&q=%s' %(formatted), colour=0x32441c)
        em.set_author(name= 'Search results for: ' + (combargs) ,icon_url='https://cdn.discordapp.com/attachments/486611168891502624/488904081369333772/search-flat.png')
        em.set_footer(text='Search generated by: %s' %(message.author) , icon_url= message.author.avatar_url )
        await client.send_message(message.channel, embed=em )
        
  if message.content.startswith('w!urban'):
        await client.send_typing(message.channel)
        args = message.content.split(" ")
        combargs = (" ".join(args[1:]))
        formatted = combargs.replace(" ", "+")
        em = discord.Embed(title=  (" ".join(args[1:])), url='https://www.urbandictionary.com/define.php?term=%s' %(formatted), colour=0x32441c)
        em.set_author(name= 'Urban search results for: ' + (combargs) ,icon_url='https://cdn.discordapp.com/attachments/486611168891502624/488904081369333772/search-flat.png')
        em.set_footer(text='Search generated by: %s' %(message.author) , icon_url= message.author.avatar_url )
        await client.send_message(message.channel, embed=em )
        
  await client.process_commands(message)
    
@client.command(pass_context=True)
async def help(ctx):
  author = ctx.message.author

  embed = discord.Embed(
    colour = discord.Colour.green()
  )

  embed.set_author(name='Commands:')
  embed.add_field(name='w!say', value='Makes the bot say something', inline=False)
  embed.add_field(name='w!userinfo', value='Shows info of a user', inline = False)
  embed.add_field(name='w!serverinfo', value='Shows server info', inline=False)
  embed.add_field(name='w!clear', value='Clear messages', inline=False)
  embed.add_field(name='w!kick', value='Kicks a user', inline=False)

  await client.send_message(author, embed=embed)
  await client.say('DMed you a message containing all the commands!')

#Fun commands
@client.command(pass_context = True)
async def say(ctx, *args):
    mesg = ' '.join(args)
    await client.delete_message(ctx.message)
    return await client.say(mesg)

@client.command(pass_context=True)
async def coinflip(ctx):
    pick = ['heads','tails']
    flip = random.choice(pick)
    await client.say ("The coin landed on " + flip + '!')
    return

@client.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's the info.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)
    return

@client.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's the info.", color=0x00ff00)
    embed.set_author(name="Server Info:")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await client.say(embed=embed)
    return 

@client.command(pass_context=True)
async def uptime(ctx):
    now = datetime.utcnow()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="WrongBot's Uptime", value="I've been online for **{elapsed.days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds")
    await client.say(embed=embed)
  
#Moderation commands
@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear (ctx, amount=100):
  if ctx.message.author.server_permissions.manage_messages:
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
      messages.append(message)
    await client.delete_messages(messages)
    await client.say('Message cleared')
    return 

@client.command(pass_context=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    author = ctx.message.author
    server = ctx.message.server
    if ctx.message.author.server_permissions.kick_members:
        if user is None:
            embed = discord.Embed(color=0xff0000)
            embed.set_author(name='Error!')
            embed.add_field(name=' :no_entry_sign: **Error** :no_entry_sign:', value='Please specify a user!', inline=False)
            embed.set_footer(text='Try again.')
            await client.say(embed=embed)
            return 
        else:
            embed = discord.Embed(color=0xff00e6)
            embed.set_author(name='Kick Information')
            embed.add_field(name='**Server:', value='**{}**'.format(server.name), inline=False)
            embed.add_field(name='**Reason:**', value='**{0}**'.format(reason), inline=True)
            embed.add_field(name='**Author:**', value='**{}**'.format(author.name), inline=False)
            await client.send_message(user, embed=embed)
            await client.kick(user)
            #Sends the user a message when he is kicked!
            embed = discord.Embed(color=0xff00e6)
            embed.set_author(name='Kick Information')
            embed.add_field(name='**Server:', value='**{}**'.format(server.name), inline=False)
            embed.add_field(name='**Reason:**', value='**{0}**'.format(reason), inline=True)
            embed.add_field(name='**Author:**', value='**{}**'.format(author.name), inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            await client.say(embed=embed)
            return 
    else:
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name=':no_entry_sign: **Error** :no_entry_sign:', value='You are missing the following permission: Kick member.', inline=False)
        embed.set_footer(text='You cant use this command!')
        await client.say(embed=embed)
        return 

@client.command(pass_context=True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
    author = ctx.message.author
    server = ctx.message.server
    if ctx.message.author.server_permissions.ban_members:
        if user is None:
            embed = discord.Embed(color=0xff0000)
            embed.set_author(name='You made a error!')
            embed.add_field(name=' :no_entry_sign: **Error** :no_entry_sign:', value='Please specify a user!', inline=False)
            embed.set_footer(text='Try again')
            await client.say(embed=embed)
            return 
        
        else:
            embed = discord.Embed(color=0xff00e6)
            embed.set_author(name='Ban - Information')
            embed.add_field(name='**Server:', value='**{}**'.format(server.name), inline=False)
            embed.add_field(name='**Reason:**', value='**{0}**'.format(reason), inline=True)
            embed.add_field(name='**Author:**', value='**{}**'.format(author.name), inline=False)
            await client.send_message(user, embed=embed)
            await client.ban(user)
            #Sends the user a message when he is kicked!
            embed = discord.Embed(color=0xff00e6)
            embed.set_author(name='Ban - Information')
            embed.add_field(name='**Server:', value='**{}**'.format(server.name), inline=False)
            embed.add_field(name='**Reason:**', value='**{0}**'.format(reason), inline=True)
            embed.add_field(name='**Author:**', value='**{}**'.format(author.name), inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            await client.say(embed=embed)
            return 
 
    else:
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name=':no_entry_sign: **Error** :no_entry_sign:', value='You are missing the following permission: Ban member', inline=False)
        embed.set_footer(text='You cant use this command!')
        await client.say(embed=embed)
        return
        
starttime = datetime.utcnow()
client.loop.create_task(change_status())
client.run(os.environ.get('BOT_TOKEN'))
