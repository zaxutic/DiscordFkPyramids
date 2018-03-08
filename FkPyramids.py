import discord
from discord.ext import commands
import asyncio
import os
import datetime
import time
import logging

Owner = 135678905028706304  # Put your user ID here

logger = logging.getLogger('discord')
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

Client = discord.Client()
bot = commands.Bot(command_prefix="!")
commandsList = {}
incomsList = {}
modcomsList = {}
regmodcoms = ["!pyramid", '!fpaddcom', '!fpdelcom', '!fpaddincom',
              '!fpdelincom', '!fpaddmodcom', '!fpdelmodcom', '!fpreact', '!s',
              '!fpgame', '!fpreact', '!fpwhitelist']
admins = [Owner]
cooldown = 0
Channels = {}

with open("commands.txt", "r", encoding="utf-8") as commandsFile:
    for line in commandsFile:
        lineParts = line.split()
        try:
            commandsList[lineParts[0].lower()] = " ".join(lineParts[1:])
        except IndexError:
            pass
with open("users.txt", "r", encoding='utf-8') as userFile:
    userList = [int(line[:-1]) for line in userFile]
with open("incoms.txt", "r", encoding='utf-8') as incomsFile:
    for line in incomsFile:
        lineParts = line.split()
        try:
            incomsList[lineParts[0].lower()] = ' '.join(lineParts[1:])
        except:
            pass
with open("modcoms.txt", "r", encoding='utf-8') as modcomsFile:
    for line in modcomsFile:
        lineParts = line.split()
        try:
            modcomsList[lineParts[0].lower()] = ' '.join(lineParts[1:])
        except:
            pass
with open("token.txt", 'r') as tokenFile:
    token = tokenFile.readline()[:-1]


def currentTime():
    t = datetime.datetime.now()
    return "{:%H:%M:%S} ".format(t)


def delete(chan):
    try:
        del Channels[chan]
    except KeyError:
        pass


@bot.event
async def on_ready():
    global noBlockUsers
    print(currentTime(), "Bot Online")
    print("Name:", bot.user.name)
    print("ID:", bot.user.id)
    noBlockUsers = [bot.user.id]
    await bot.change_presence(game=discord.Game(
        name="pyramids getting fk'd", type=3))


@bot.event
async def on_message(message):
    global voice
    global vChannel
    global cooldown
    username = str(message.author)
    mention = message.author.mention
    userId = message.author.id
    msg = str(message.content)
    msgParts = msg.split()
    channel = message.channel
    chanId = channel.id
    guild = message.guild
    guildId = guild.id
    print('{} {}: {}'.format(currentTime(), username, msg))
    com = None
    com2 = None
    com3 = None
    try:
        com = msgParts[0].lower()
        com2 = msgParts[1].lower()
        com3 = msgParts[2]
    except:
        pass

    if isinstance(channel, discord.abc.PrivateChannel):
        if chanId in Channels:
            x = 1
            if len(msgParts) == 1:
                if (len(msgParts) == Channels[chanId]['len'] - 1 and
                    msg == Channels[chanId]['py']):
                    await channel.send(
                        "Baby pyramids don't count, you fucking degenerate.")
                Channels[chanId]['py'] = msg
                Channels[chanId]['len'] = 1
            elif len(msgParts) == 1 + Channels[chanId]['len']:
                Channels[chanId]['len'] += 1
                for part in msgParts:
                    if part != Channels[chanId]['py']:
                        delete(chanId)
                        x = 0
                        break
                if x:
                    if Channels[chanId]['len'] == 3:
                        await channel.send("no")
                        delete(chanId)
            else:
                delete(chanId)
        elif len(msgParts) == 1:
            Channels[chanId] = {'len': 1, 'py': msg}

        if userId == Owner:
            if com == '!send':
                if len(msgParts) >= 3:
                    await bot.get_channel(int(com2)).send(' '.
                        join(msgParts[2:]))
    else:
        if chanId in Channels:
            if userId not in noBlockUsers:
                x = 1
                if len(msgParts) == 1:
                    if (len(msgParts) == Channels[chanId]['len'] - 1 and
                        msg == Channels[chanId]['py']):
                        await channel.send("Baby pyramids don't count,"
                            "you fucking degenerate {}.".format(mention))
                    Channels[chanId]['py'] = msg
                    Channels[chanId]['len'] = 1
                elif len(msgParts) == 1 + Channels[chanId]['len']:
                    Channels[chanId]['len'] += 1
                    for part in msgParts:
                        if part != Channels[chanId]['py']:
                            delete(chanId)
                            x = 0
                            break
                    if x:
                        if Channels[chanId]['len'] == 3:
                            await channel.send("no")
                            delete(chanId)
                else:
                    delete(chanId)
            else:
                delete(chanId)
        elif len(msgParts) == 1:
            Channels[chanId] = {'len': 1, 'py': msg}

    if userId != bot.user.id:
        if com in commandsList:
            await channel.send(commandsList[com])
        elif time.time() - cooldown > 30:
            for key in incomsList:
                if key in msg.lower():
                    await channel.send(incomsList[key])
                    break
            cooldown = time.time()
        if com in ['color', 'colour'] and guildId == 311016926925029376:
            # Requires "Manage Roles" permission
            if com2:
                colorHex = com2.strip('#')
                lst = ['a', 'b', 'c', 'd', 'e', 'f']
                isHex = True

                for char in colorHex:
                    if not char.isdigit() and char not in lst:
                        isHex = False
                        break

                if isHex:
                    await channel.send(
                        "{} Setting color to #{}".format(mention, colorHex))
                    for r in message.author.roles:
                        if r.name.startswith('#'):
                            await message.author.remove_roles(r)
                    for r in guild.roles:
                        if r.name == '#' + colorHex:
                            await message.author.add_roles(r)
                            break
                    else:
                        colorRole = await guild.create_role(name="#" + colorHex,
                            colour=discord.Colour(value=int(colorHex, 16)))
                        await colorRole.edit(position=len(guild.roles) - 8)
                        await message.author.add_roles(colorRole)
                    await channel.send(
                        "{} Set colour to #{}".format(mention, colorHex))
                else:
                    await channel.send("{} Syntax: `{} [{} hex code]`".
                        format(mention, com, com[1:]))
            else:
                await channel.send("{} Syntax: `{} [{} hex code]`".
                    format(mention, com, com[1:]))
        elif com == '!fpcommands':
            await channel.send(mention + " Commands: " +
                ', '.join(commandsList.keys()))
        elif com == '!fpadmins':
            await channel.send(mention +  " Admins: " + ', '.join(userList))
        elif com == '!fpincoms':
            await channel.send(mention + " In_commands: " +
                ', '.join(incomsList.keys()))
        elif com == '!fpmodcoms':
            await channel.send(mention + " Mod commands: " +
                ', '.join(modcomsList + regmodcoms))
        elif com == '!nobully':
            nobullyEmbed = discord.Embed(description="**Don't Bully!**")
            nobullyEmbed.set_image(url="https://i.imgur.com/jv7O5aj.gif")
            await channel.send(embed=nobullyEmbed)

    if userId in userList + admins:
        if com == "!pyramid" and len(msgParts) >= 3:
            p = ' '.join(msgParts[2:]) + ' '
            pLen = int(com2) + 1
            for i in range(1, pLen):
                await channel.send(p * i)
            for i in range(2, pLen):
                await channel.send(p * (pLen - i))
        elif com == "!delmsg":
            # Requires "Manage Messages" permission
            if com2.isdigit():
                com2 = int(com2)
                async for m in channel.history(limit=com2):
                    try:
                        await m.delete()
                    except discord.errors.Forbidden:
                        print("Insufficient permissions")
                        pass
        elif com == "!fpaddcom":
            if len(msgParts) >= 3:
                with open("commands.txt", "a",
                    encoding="utf-8") as commandsFile:
                    commandsList[com2] = " ".join(msgParts[2:])
                    commandsFile.write(' '.join(msgParts[1:]) + '\n')
                await channel.send('{} Added command "{}"'.format(mention,com2))
            else:
                await channel.send(mention +
                    " Syntax: `!fpaddcom [command] [output]`")
        elif com == '!fpdelcom':
            if len(msgParts) == 2:
                if com2 in commandsList:
                    del commandsList[com2]
                    with open('commands.txt') as f:
                        lines = f.readlines()
                    with open("commands.txt", 'w',
                        encoding='utf-8') as commandsFile:
                        for line in lines:
                            if not line.split()[0] == com2:
                                commandsFile.write(line + '\n')
                    await channel.send(
                        '{} Removed command "{}"'.format(mention, com2))
                else:
                    await channel.send(mention + ' Command "{}" doesn\'t exist'.
                        format(com2))
            else:
                await channel.send("Syntax: `!fpdelcom [command]`")
        elif com == "!fpaddincom":
            with open("incoms.txt", "a", encoding='utf-8') as incomsFile:
                incomsFile.write(' '.join(msgParts[1:]) + '\n')
                incomsList[com2] = ' '.join(msgParts[2:])
            await channel.send('{} Added in_command "{}"'.format(mention, com2))
        elif com == '!fpdelincom':
            if com2 in incomsList:
                del incomsList[com2]
                with open('incoms.txt') as f:
                    lines = f.readlines()
                with open("incoms.txt", "w", encoding='utf-8') as incomsFile:
                    for line in lines:
                        if not line.split()[0] == com2:
                            incomsFile.write(line + '\n')
                await channel.send(
                    '{} Removed in_command "{}"'.format(mention, com2))
            else:
                await channel.send('{} In_command "{}" doesn\'t exist'.
                    format(mention, com2.capitalize))
        elif com == '!fpaddmodcom':
            with open("modcoms.txt", "a", encoding="utf8") as modcomsFile:
                modcomsList[com2] = " ".join(msgParts[2:])
                modcomsFile.write(' '.join(msgParts[1:] + '\n'))
            await channel.send(
                '{} Added mod command "{}"'.format(mention, com2))
        elif com == '!fpdelmodcom':
            if len(msgParts) == 2:
                del modcomsList[com2]
                with open('modcoms.txt') as f:
                    lines = f.readlines()
                with open("modcoms.txt", "w", encoding="utf-8") as modcomsFile:
                    for line in lines:
                        if line:
                            if not line.split()[0].lower() == com2:
                                modcomsFile.write(line + '\n')
                await channel.send(
                    '{} Deleted mod command "{}"'.format(mention, com2))
        elif com == '!fpdelroles':
            # Requires "Manage Roles" permission.
            # Doesn't usually delete all roles at once,
            # requires multiple executions.

            # Commented code for debugging

            roles = guild.roles
            members = guild.members
            # print("Roles:", (len(roles))
            # print("Roles:", ', '.join([r.name for r in roles]))
            usedRoles = []
            for r in roles:
                for u in members:
                    if r in u.roles:
                        usedRoles.append(r)
                        break
            # print("Used:", ', '.join([r.name for r in usedRoles]))
            for r in usedRoles:
                roles.remove(r)
            # print("Unused:", ', '.join([r.name for r in roles]))
            for r in roles:
                await r.delete()
                await channel.send('Deleted role "{}".'.format(r.name))
            await channel.send("Deleted unused roles.")
        elif com == '!fpreact':
            num = int(com2)
            if com3.isdigit():
                for em in bot.emojis():
                    if em.id == com3:
                        e = em
                        async for i in channel.history(limit=num):
                            await i.add_reaction(e)
                        break
            else:
                e = com3
                try:
                    async for i in channel.history(limit=num):
                        await i.add_reaction(e[2:-1])
                except:
                    await channel.send(mention +
                        ' Syntax: `!fpreact [n] [emote]`')
        elif com == '!fpwhitelist':
            if com2.isdigit():
                noBlockUsers.append(com2)
            else:
                await channel.send(mention +
                    ' Syntax: `!fpwhitelist [user id]`')
        elif com == '!fpblacklist':
            if com2.isdigit():
                if com2 in noBlockUsers:
                    noBlockUsers.remove(com2)
                else:
                    await channel.send('{} {} is not whitelisted'.format(
                        mention, com2))
            else:
                await channel.send(mention + ' Syntax: `!fpwhitelist [user id]`')

        if com in modcomsList:
            await channel.send(modcomsList[com])
        elif com == "!s" and len(msgParts) >= 3:
            n = int(com2)
            for i in range(n):
                await channel.send(' '.join(msgParts[2:]))
        elif com == "!fpstatus":
            await bot.change_presence(game=discord.Game(
                name=' '.join(msgParts[2:]), type=int(com2)))
            await channel.send(mention + ' Set game to "{}"'.format(
                ' '.join(msgParts[1:])))
        elif com == '!fpvoice':  # Incomplete
            if len(msgParts) >= 2:
                if com2 == 'join':
                    if len(msgParts) == 3:
                        vChannel = bot.get_channel(int(com3))
                    elif len(msgParts) == 2:
                        vChannel = message.author.voice.channel
                    voice = await vChannel.connect()
                    await channel.send('Joined "{}"'.format(vChannel.name))
                elif com2 == 'leave':
                    for c in bot.voice_clients:
                        if c.guild == guild:
                            await voice.disconnect()
                            await channel.send('Left "' + vChannel.name + '"')
            else:
                await channel.send('Missing argument: `join`, `leave`')

    if userId in admins:
        if com == "!fpadduser" and len(msgParts) == 2:
            if message.mentions:
                user = message.mentions[0].id
            else:
                user = int(com2)
            with open("users.txt", "a", encoding='utf-8') as userFile:
                userFile.write(str(user) + '\n')
                userList.append(user)
            await channel.send('{} Added {} to admins'.format(mention, user))
        elif com == "!fpdeluser":
            if message.mentions:
                user = message.mentions[0].id
            else:
                user = str(com2)
            userList.remove(user)
            with open('users.txt') as f:
                lines = f.readlines()
            with open("users.txt", "w", encoding='utf-8') as userFile:
                for line in lines:
                    if line[:-1] != str(user):
                        userFile.write(line)
            await channel.send('{} Removed {} from admins.'.format(mention,
                user))
        elif com == "!fpshutdown":
            await channel.send('Shutting down client.')
            await bot.close()
            print(currentTime, "Bot shutdown.")

bot.run(token)
