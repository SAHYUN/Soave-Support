import discord
from discord.ext import commands
import typing
import datetime
import json

client = commands.Bot(command_prefix= ".")

@client.event
async def on_ready():
    print("Ready")

@client.command()
@commands.has_permissions(ban_members= True)
async def ban(ctx, members: commands.Greedy[discord.Member], delete_days: typing.Optional[int] = 0, *, reason: str = "사유가 입력되지 않았습니다."):
    channel = client.get_channel()
    now = datetime.datetime.now()
    now = now.strftime("%Y.%m.%d %H:%M:%S")
    for member in members:
        await member.ban(delete_message_days= delete_days, reason= reason)

        embed = discord.Embed(title= "차단이 발생하였습니다!", description= f"차단 발생 시각 : {now}")
        embed.add_field(name= "관리자", value= ctx.author.mention, inline= False)
        embed.add_field(name= "유저", value= member.mention, inline= False)
        embed.add_field(name= "사유", value= reason, inline= False)
        await channel.send_message(embed= embed)


@client.command()
@commands.has_permissions(ban_members= True)
async def unban(ctx, members: commands.Greedy[discord.Member], *, reason: str = "사유가 입력되지 않았습니다."):
    channel = client.get_channel()
    now = datetime.datetime.now()
    now = now.strftime("%Y.%m.%d %H:%M:%S")

    for member in members:
        await member.unban(reason= reason)

        embed = discord.Embed(title= "차단 해제가 발생하였습니다!", description= f"차단 해제 발생 시각 : {now}")
        embed.add_field(name= "관리자", value= ctx.author.mention, inline= False)
        embed.add_field(name= "유저", value= member.mention, inline= False)
        embed.add_field(name= "사유", value= reason, inline= False)
        await channel.send_message(embed= embed)


@client.command()
@commands.has_permissions(kick_members= True)
async def kick(ctx, members: commands.Greedy[discord.Member], *, reason: str = "사유가 입력되지 않았습니다."):
    channel = client.get_channel()
    now = datetime.datetime.now()
    now = now.strftime("%Y.%m.%d %H:%M:%S")
    for member in members:
        await member.kick(reason= reason)

        embed = discord.Embed(title= "추방이 발생하였습니다!", description= f"추방 발생 시각 : {now}")
        embed.add_field(name= "관리자", value= ctx.author.mention, inline= False)
        embed.add_field(name= "유저", value= member.mention, inline= False)
        embed.add_field(name= "사유", value= reason, inline= False)
        await channel.send_message(embed= embed)


@client.command()
@commands.has_permissions(kick_members= True)
async def warn(ctx, members: commands.Greedy[discord.Member], *, reason: str = "사유가 입력되지 않았습니다."):
    channel = client.get_channel()
    now = datetime.datetime.now()
    now = now.strftime("%Y.%m.%d %H:%M:%S")
    for member in members:
        embed = discord.Embed(title= "경고가 발생했습니다!", description= f"경고 발생 시각 : {now}")
        embed.add_field(name= "관리자", value= ctx.author.mention, inline= False)
        embed.add_field(name= "유저", value= member.mention, inline= False)
        embed.add_field(name= "사유", value= reason, inline= False)
        with open('warns.json', "r") as warns:
            warns_data = json.load(warns)
        
        try:
            warns_data[str(member.id)] += 1
        except:
            warns_data[str(member.id)] = 0

        warns_data[str(member.id)] += 1
        with open('warns.json', 'w') as warns:
            json.dump(warns_data, warns, indent= 4)
        embed.insert_field_at(2, name= f"{member.name} 님의 경고 횟수", value= warns_data[str(member.id)], inline= False)
        await channel.send(embed= embed)

        if warns_data[str(member.id)] == 3:
            embed_ban = discord.Embed(title= "차단이 발생하였습니다!", description= f"차단 발생 시각 : {now}")
            embed_ban.add_field(name= "관리자", value= "Soave 서포트", inline= False)
            embed_ban.add_field(name= "유저", value= member.mention, inline= False)
            embed_ban.add_field(name= "사유", value= "경고 3회 누적", inline= False)
            await member.ban(reason= "경고 3회 누적", delete_message_days= 1)
            await channel.send(embed= embed_ban)

            del warns_data[str(member.id)]
            with open('warns.json', 'w') as warns:
                json.dump(warns_data, warns, indent= 4)



client.run()