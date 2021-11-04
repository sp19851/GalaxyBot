import discord
from keep_alive import keep_alive
import os
from discord.ext import commands
from discord.ext.commands import Bot
from discord import embeds
from typing import Union
import random

import asyncio
import traceback

intents = discord.Intents.all()
#client = discord.Bot(intents = intents)
bot = commands.Bot(command_prefix='!', intents=intents)

# отображение статуса бота
@bot.event
async def on_ready():
    activity = discord.Game(name="GalaxyRP FiveM", type=3) 
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("LocalBot is ready")

# сообщение о присоеденению к серверу нового игрока
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Гость') #роль по умолчанию
    await member.add_roles(role)
    wellcome_table = discord.Embed(title="",
                                   url="https://realdrewdata.medium.com/",
                                   description="",
                                   color=0x2ecc71)
    wellcome_table.set_author(name="Бортпроводник", url="", icon_url="")
    wellcome_table.set_thumbnail(
        url=
        'https://blog.aci.aero/wp-content/uploads/2019/03/shutterstock_745544935-952x635.jpg'
    )
    wellcome_table.add_field(name="В штат прибыл рейс №",
                             value="{}".format(random.randint(10000, 99990)),
                             inline=False)
    wellcome_table.add_field(
        name="Просьба пропустить пассажира бизнес класса  ",
        value="{}".format(member),
        inline=False)
    wellcome_table.set_footer(text="Galaxy AirLines")
    channel = bot.get_channel(904124202473373716)
    await channel.send(embed=wellcome_table)
    await member.send(
        "Вы присоединились к серверу {}!  Роль по умолчанию: {}."
        .format(member.guild.name, role.name))
    print("{} joined to server! Role: {}".format(member, role.id))

# сообщение о том, что кто то ливнул
@bot.event
#async def on_member_leave(member):
async def on_member_remove(member):
    print("leave to channel! ")
    channel = bot.get_channel(904124202473373716)
    await channel.send("{} leave from server!".format(member.name))
    By_table = discord.Embed(title="",
                             url="https://realdrewdata.medium.com/",
                             description="",
                             color=0xFF5733)
    By_table.set_author(name="Бортпроводник", url="", icon_url="")
    By_table.set_thumbnail(
        url=
        'https://img3.goodfon.ru/wallpaper/nbig/5/d8/art-samolet-polet-solnce-nebo.jpg'
    )
    By_table.add_field(name="Штат покидает рейс №",
                       value="{}".format(random.randint(10000, 99990)),
                       inline=False)
    By_table.add_field(name="Просьба уступить место пассажиру ",
                       value="{}".format(member),
                       inline=False)
    By_table.set_footer(text="Galaxy AirLines")
    await channel.send(embed=By_table)
    print("{} leave from server!".format(member))


# Получение роли после нажатия эмоции пользователем под прочтением правил
channels = [857320946330763275, 903992273593843732, 903992194090807376] #0-канал  с правилами (первая роль(по умолчанию), присваивается когда просто залетаешь, вторая по реакции об ознакомлении с правилами, третья при нажатии админами для вайтлиста)  1-канал откуда создаются  тикеты  2-канал с правилами
categID = 904275651123626015 #категория каналов с тикетами
SUPPORT_ROLE_ID = 904320771759943781 #роль поддержки, для тикетов


@bot.event
async def on_raw_reaction_add(payload):
    chan = bot.get_channel(payload.channel_id)
    mess = await chan.fetch_message(payload.message_id)
    user1 = payload.member
    user2 = mess.author
    print(mess)
    user2 = mess.author
    adm = payload.member
    perms = adm.guild_permissions
    is_admin = perms.administrator
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    if not mess.id in channels and chan.id not in channels:
        return
    elif mess.id == channels[0]:

        role = user1.guild.get_role(854001171542310942) #вторая роль
        await user1.add_roles(role)
    elif chan.id == channels[2] and is_admin:
        role = discord.utils.get(user2.guild.roles, name='Whitelist')
        await user2.add_roles(role)
        
    elif chan.id == channels[1]:  # реакция в канале поддержка
        
        category = guild.get_channel(categID)
        support_role = guild.get_role(SUPPORT_ROLE_ID)
        print("work1", categID, user1, support_role)
        overwrites = {
            guild.default_role:
            discord.PermissionOverwrite(read_messages=False),
            payload.member:
            discord.PermissionOverwrite(read_messages=True,
                                        send_messages=True),
            support_role:
            discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await category.create_text_channel(name=f'ticket - {user1}',
                                           overwrites=overwrites)
        await channel.send(f"{user1.mention}")
       
        # Создём emb
        #emb = discord.Embed( title = f'Тикет #{ticket_id}', description = '', colour = discord.Color.red() )
        emb = discord.Embed( title = f'Тикет', description = '', colour = discord.Color.red() )
        emb.set_author(name = user1, icon_url = user1.avatar_url)
        #emb.add_field( name = 'Команды', value = f'`{prefix}voice`', inline=False)
        emb.add_field( name = 'Команды', value = f'`!closeT`  `!deleteT`', inline=False)
        emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/sonya/swarm/128/Ticket-icon.png")
        await channel.send(embed=emb)
        #await ctx.send(f':tickets: Тикет {ticket_id} создан! (<#{channel.id}>)')
    else:
        return

    channel = bot.get_channel(904289734497558569) # служебный канал
    if is_admin:
        await channel.send(
            "Пользователь {} c правами admin нажал реакцию".format(adm))
    else:
        await channel.send(
            "Пользователь {} c правами not admin нажал реакцию {}".format(adm))

#закрываем тикет
@bot.command()
async def closeT(ctx):
    channel_name = (ctx.message.channel.name)
    guild_id = str(ctx.message.guild.id)
    print('close', channel_name, guild_id)
    
    channel = ctx.message.channel



    # Создаём оверрайт-права
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    overwrite.read_messages = True
    overwrite.read_message_history = True
    overwrite.attach_files = False
    overwrite.view_channel = False
    counter = 0
    async for message in channel.history(limit=200):
        #if message.author == client.user:
        counter += 1  
        print(counter, message.author)
        if counter <= 1 :
          author = message.author
          print('Autor', message.author)
          # Удаляем права с создателя
          await channel.set_permissions(author, overwrite=overwrite)

          await asyncio.sleep(1)
          await channel.send(f"Тикет закрыт")
          return
      
    
    
   

#удаляем тикет
SUPPORTROLE = "Galaxy"
@bot.command()
@commands.has_any_role(SUPPORTROLE)
async def deleteT(ctx): #, member: discord.Member = None):
    channel_name = (ctx.message.channel.name)
    guild_id = ctx.message.guild.id
    guild = bot.get_guild(guild_id)
    channel = ctx.message.channel
    #print('delete', guild_id, guild, SUPPORTROLEID)
    #support_role = guild.get_role(SUPPORTROLEID)
    mess = channel.last_message
    user = mess.author
    #perm = channel.permissions_for(user)
    #print('delete2', support_role, user, perm)
    await channel.delete()
    

    
  




# Команда написания текста от имени бота
@bot.command()
async def text(ctx, *, text):
    await ctx.send(f'{text}')
    await ctx.message.delete()
    channel = bot.get_channel(904289734497558569) # служебный канал
    is_admin = ctx.author.guild_permissions.administrator
    print('is_admin', is_admin)
    if is_admin:
        await channel.send(
            "Пользователь {} c правами admin применил команду {}".format(
                ctx.author.name, ctx.message.content))
    else:
        await channel.send(
            "Пользователь {} c правами not admin применил команду {}".format(
                ctx.author.name, ctx.message.content))


#Получение именя по id
@bot.command()
async def getuserbyid(ctx, userid: int):
    await ctx.message.delete()
    _member = await ctx.guild.fetch_member(userid)

    await ctx.send("```id {} использует член сообщества {}/{}```".format(
        userid, _member, _member.nick))
    is_admin = ctx.author.guild_permissions.administrator
    channel = bot.get_channel(904289734497558569) # служебный канал
    if is_admin:
        await channel.send(
            "Пользователь {} c правами admin применил команду {}".format(
                ctx.author.name, ctx.message.content))
    else:
        await channel.send(
            "Пользователь {} c правами not admin применил команду {}".format(
                ctx.author.name, ctx.message.content))


@getuserbyid.error
async def getuserbyid_error(ctx, error):
    await ctx.send(error)


#Удаление сообщений
@bot.command()
@commands.has_any_role(SUPPORTROLE)
async def clearmes(ctx, number):
    adm = ctx.message.author
    perms = adm.guild_permissions
    is_admin = perms.administrator
    #if is_admin:
    number = int(number)  #Converting the amount of messages to delete to an integer
    ch = ctx.message.channel
    deleted = await ch.purge(limit=number, check=clearmes)
    await ch.send("```{} удалил {} сообщения(й)```".format(
           adm, len(deleted)))
    #else:
    #    return
    print('clearmes', SUPPORTROLE)
    channel = bot.get_channel(904289734497558569) # служебный канал
    if is_admin:
        await channel.send(
            "Пользователь {} c правами admin применил команду {}".format(
                ctx.author.name, ctx.message.content))
    else:
        await channel.send(
            "Пользователь {} c правами not admin применил команду {}".format(
                ctx.author.name, ctx.message.content))


@clearmes.error
async def getuserbyid_error(ctx, error):
    await ctx.send(error)


keep_alive()

token = os.environ['DISCORD_BOT_SECRET']
bot.run(token)
