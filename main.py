import discord
from discord.ext import commands
import logging
import dotenv
import os
import discord.utils
import random
import time
from google import genai

# loading enviroment
dotenv.load_dotenv()

# bot initiation
token = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# ai initialization
ai_token = os.getenv("AI_TOKEN")
ai_client = genai.Client(api_key=ai_token)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1414803871456301149)
    await channel.send(f"Welcome {member.mention} to learn AI")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1414803871456301149)
    await channel.send(f"{member.mention} has been kicked")


@bot.command()
async def assign_role(ctx, c: str = "no member", *roles_give):
    # will give None if not present
    if len(roles_give) == 1:
        r = roles_give[0]
        role_present = discord.utils.get(ctx.guild.roles, name=r)

    # check if assign have person and role
    if c == "no member" or len(roles_give) != 1:
        if len(roles_give) != 1:
            await ctx.send(
                'role can only be given one at the time "!assign @member role"'
            )
            return
        await ctx.send('assign need to be accompany with user "!assign @member role"')
        return
    # checking if person was mention or not
    elif c.startswith("<@") == False and c.endswith(">") == False:
        await ctx.send('assign need to be accompany with user "!assign @member role"')
        return
    # checking if role is available in the channel or not
    elif role_present == None:
        await ctx.send(f"we don't have role with name {r}")
        return
    # checking if assigner have authorization or not
    else:
        auth_member = ctx.author
        does_have_auth = False
        for role in auth_member.roles:
            if role.name == "gamer":
                does_have_auth = True
                break
        if not does_have_auth:
            await ctx.send("you don't have auth to assign role")
            return

    # chaing user id str to id str
    c = int(c[2:-1])

    # checking if person already have that role
    mentioned_member = ctx.guild.get_member(c)
    for role in mentioned_member.roles:
        if role.name == r:
            await ctx.send("this member already have the role")
            return

    await mentioned_member.add_roles(role_present)
    await ctx.send(f"{r} role has been assigned to {mentioned_member} ")


@bot.command()
async def remove_role(ctx, c="no member", *roles_give):
    # will give None if not present
    if len(roles_give) == 1:
        r = roles_give[0]
        role_present = discord.utils.get(ctx.guild.roles, name=r)

    # check if assign have person and role
    if c == "no member" or len(roles_give) != 1:
        if len(roles_give) != 1:
            await ctx.send(
                'role can only be given one at the time "!assign @member role"'
            )
            return
        await ctx.send('assign need to be accompany with user "!assign @member role"')
        return
    # checking if person was mention or not
    elif c.startswith("<@") == False and c.endswith(">") == False:
        await ctx.send('assign need to be accompany with user "!assign @member role"')
        return
    # checking if role is available in the channel or not
    elif role_present == None:
        await ctx.send(f"we don't have role with name {r}")
        return
    # checking if assigner have authorization or not
    else:
        auth_member = ctx.author
        does_have_auth = False
        for role in auth_member.roles:
            if role.name == "gamer":
                does_have_auth = True
                break
        if not does_have_auth:
            await ctx.send("you don't have auth to assign role")
            return

    # chaing user id str to id str
    c = int(c[2:-1])

    # checking if person already have that role
    mentioned_member = ctx.guild.get_member(c)
    does_have_role = False
    for role in mentioned_member.roles:
        if role.name == r:
            does_have_role = True
            break
    if not does_have_role:
        await ctx.send("user does have that role")
        return

    if mentioned_member == ctx.author:
        await ctx.send("self removing roles can't be done")
        return
    await mentioned_member.remove_roles(role_present)
    await ctx.send(f"{r} role has been removed from {mentioned_member} ")


@bot.command()
async def kick_user(ctx, c: str = "no member"):
    # checking given arguments
    if c == "no member" or c.startswith("<@") == False:
        await ctx.send('to kick user you have to "!kick_user @member"')
        return
    else:
        # if user have auth
        does_have_auth = False
        for role in ctx.author.roles:
            if role.name == "gamer":
                does_have_auth = True
                break
        # if
        if not does_have_auth:
            print([ctx.author.roles])
            await ctx.send(
                'you do not have the authorization to use command "!kick_user"'
            )
            return
    c = int(c[2:-1])
    mention_member = ctx.guild.get_member(c)
    if mention_member == ctx.author:
        await ctx.send("self kicking is not allowed")
        return
    print(mention_member)
    if mention_member == None:
        await ctx.send('to kick user you have to "!kick_user @member"')
        return
    await mention_member.kick(reason="spam")


@bot.command()
async def ban_user(ctx, member: discord.Member):
    # check user have permission
    # check if it self banning
    try:
        does_have_auth = False
        for role in ctx.author.roles:
            if role.name == "gamer":
                does_have_auth = True
                break
        if not does_have_auth:
            await ctx.send(f"{ctx.author} does not have permission")
            return
        elif ctx.author == member:
            await ctx.send("self banning is not allowed")
            return
        else:
            await member.ban(reason="test")
            return
    except discord.Forbidden:
        await ctx.send("permisson is not allowed")
    except discord.HTTPException:
        await ctx.send("ban_user api error")


@ban_user.error
async def ban_user_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: "!ban_user @member"')
        return
    elif isinstance(error, commands.UserNotFound):
        await ctx.send("user not found")
        return
    else:
        await ctx.send("user not found")


@bot.command()
async def coinflip(ctx, c):
    choices = ["head", "tail"]
    c = c.strip().lower()
    if c not in choices:
        await ctx.message.add_reaction("😵")
        await ctx.send('To play coinflip "!coinflip head or tail"')
        return
    c_choice = random.choice(choices)
    if c_choice == c:
        await ctx.message.add_reaction("👍")
        await ctx.send(f"You won!, It was {c_choice.capitalize()}")
    else:
        await ctx.message.add_reaction("👎")
        await ctx.send(f"Sorry you lost!, It was {c_choice.capitalize()}")


@bot.command()
async def check_members(ctx):
    all_members = ctx.guild.members
    for i in all_members:
        await ctx.send(i.name)


@bot.command()
async def check_roles(ctx, member: discord.Member):
    await ctx.send(f"{member.mention} has following roles ")
    for role in member.roles:
        if role.name == "@everyone":
            await ctx.send("everyone")
        else:
            await ctx.send(role.name)


@check_roles.error
async def check_roles_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: "!check_roles @member"')
    elif isinstance(error, commands.UserNotFound):
        await ctx.send("user not found")
    else:
        await ctx.send("user not found")


@bot.command()
async def hey_ai(ctx, *c):

    if len(c) == 0:
        await ctx.send('hello... to use !hey_ai command do "!hey_ai message"')
        return

    if ctx.channel.id != 1414807392205672561:
        await ctx.send(
            f'Use "hey_ai message" command in <#{1414807392205672561}> channel'
        )
        return

    asked_q = " ".join(c)
    response = ai_client.models.generate_content_stream(
        model="gemini-2.0-flash-001",
        contents=f"Prompt rules: 1.Give answer under 500 words, 2.Make it informative but shot, 3.Give learning resources if it is a learning questions, 4.Other wise talk normally under 500 word ruls, 5.answer should be under 500 words and don't reiterate the prompt-This is the question or chat -> {asked_q}",
    )
    await ctx.send("bot is thinking...🤖")
    time.sleep(2)
    for c in response:
        await ctx.send(c.text)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)

