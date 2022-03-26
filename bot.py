import discord
import sqlite3
from discord.ext import commands
from discord.utils import get
from to import T, TB, J, JB, M, MB, A, AB, S, SB
from my_db import DB
from my_game import Game, Team, User

db = DB()
game = Game()

bot = commands.Bot(command_prefix='!')
db.create_table()

@bot.event
async def on_ready():
    print('로그인중입니다. ')
    print(f"봇={bot.user.name}로 연결중")
    print('연결이 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command()
async def 도움말(ctx):
    help_str = ''
    help_str += '!등록 탑 정글 미드 원딜 서폿\n'
    help_str += 'ex) !등록 탑 정글\n'
    help_str += '\n'
    help_str += '!모집\n'
    help_str += '!모집취소\n'
    help_str += '\n'
    help_str += '!참가\n'
    help_str += '!참가취소\n'
    help_str += '\n'
    help_str += '!시작\n'
    help_str += '\n'
    help_str += '!매물\n'
    help_str += '\n'
    help_str += '!팀장 1팀팀장 2팀팀장 포지션(탑/정글/미드/원딜/서폿)\n'
    help_str += 'ex) !팀장 1 2 탑\n'
    help_str += '\n'
    help_str += '!픽 매물번호 포지션(탑/정글/미드/원딜/서폿)\n'
    help_str += 'ex) !픽 1 탑\n'
    help_str += '\n'
    help_str += '!팀\n'
    help_str += '!승리 팀(1팀/2팀)\n'
    help_str += 'ex) !승리 1팀'
    embed = discord.Embed(title="도움말", description=help_str, color=0x62c1cc)
    await ctx.send(embed=embed)

@bot.command()
async def 등록(ctx, text = None):
    if text is None:
        help_str = ''
        help_str += '!등록 탑 정글 미드 원딜 서폿\n'
        help_str += 'ex) !등록 탑 정글'
        embed = discord.Embed(title="도움말", description=help_str, color=0x62c1cc)
        await ctx.send(embed=embed)
        return

    global db

    id = ctx.author.id
    name = ctx.message.author.display_name

    t = 1 if text.find("탑") != -1 else 0
    j = 1 if text.find("정글") != -1 else 0
    m = 1 if text.find("미드") != -1 else 0
    a = 1 if text.find("원딜") != -1 else 0
    s = 1 if text.find("서폿") != -1 else 0
    print("{}{}{}{}{}".format(t,j,m,a,s))

    if t or j or m or a or s:
        db.regist(id, "{}{}{}{}{}".format(t,j,m,a,s))
        await ctx.send("등록 완료")
    else:
        await ctx.send('!등록 포지션(탑/정글/미드/원딜/서폿)')
        await ctx.send('ex) !등록 탑 정글')

@bot.command()
async def 내정보(ctx):
    global db

    id = ctx.author.id
    name = ctx.message.author.display_name

    ret = db.get(id)
    if ret[0] == False:
        await ctx.send(ret[1])
        return

    user = User(id, name, ret[1][1], ret[1][2], ret[1][3])
    embed = discord.Embed(title="{}님".format(user.discord_name), description="{}\n {}승 {}패".format(user.print(), user.win, user.lose), color=0x62c1cc)
    await ctx.send(embed=embed)

@bot.command()
async def 모집(ctx):
    global game

    id = ctx.author.id
    ret = game.new_game(id)
    if ret[0] == False:
        await ctx.send(ret[1])
        return

    await ctx.send(file=discord.File('image/assemble.gif'))
    await ctx.send("참가하실 분은 !참가")

@bot.command()
async def 모집취소(ctx):
    global game

    id = ctx.author.id
    ret = game.cancel_game(id)
    if ret[0] == False:
        await ctx.send(ret[1])
        return

    await ctx.send("내전이 취소되었습니다.")

@bot.command()
async def 참가(ctx):
    global db
    global game

    id = ctx.author.id
    name = ctx.message.author.display_name

    ret = db.get(id)
    if ret[0] == False:
        await ctx.send(ret[1])
        await ctx.send('!등록 포지션(탑/정글/미드/원딜/서폿)')
        await ctx.send('ex) !등록 탑 정글')

    user = User(id, name, ret[1][1], ret[1][2], ret[1][3])
    ret = game.attend(user)
    if ret[0] == -1:
        await ctx.send(ret[1])
        return

    await ctx.send("참가 완료 [{}명 참가중]". format(ret[0]))

@bot.command()
async def 참가취소(ctx):
    global db
    global game

    id = ctx.author.id
    name = ctx.message.author.display_name

    ret = db.get(id)
    if ret[0] == False:
        await ctx.send(ret[1])
        await ctx.send('!등록 포지션(탑/정글/미드/원딜/서폿)')
        await ctx.send('ex) !등록 탑 정글')

    user = User(id, name, ret[1][1], ret[1][2], ret[1][3])
    ret = game.absent(user)
    if ret[0] == -1:
        await ctx.send(ret[1])
        return

    await ctx.send("참가 취소 완료 [{}명 참가중]". format(ret[0]))

@bot.command()
async def 매물(ctx):
    global game

    mem_num = 1
    embed = discord.Embed(title="매물 정보", description="", color=0x62c1cc)
    for mem in game.participant:
        if mem.discord_id != 0 and mem.sold == False :
            embed.add_field(name="{}. {}님".format(mem_num, mem.discord_name), value="{}\n {}승 {}패".format(mem.print(), mem.win, mem.lose), inline=True)
        mem_num += 1
    await ctx.send(embed=embed)

    if len(game.participant) != 10:
        await ctx.send("아직 10명이 되지 않았습니다.")

@bot.command()
async def 시작(ctx):
    global game
    await ctx.send(game.draft()[1])

@bot.command()
async def 팀장(ctx, text = None):
    if text is None:
        help_str = ''
        help_str += '!팀장 1팀팀장 2팀팀장 포지션(탑/정글/미드/원딜/서폿)\n'
        help_str += 'ex) !팀장 1 2 탑'
        embed = discord.Embed(title="도움말", description=help_str, color=0x62c1cc)
        await ctx.send(embed=embed)
        return

    global game

    id = ctx.author.id

    strings = text.split()
    team1_master = int(strings[0])
    team2_master = int(strings[1])
    position = strings[2]
    pos_num = 0
    if position == "탑" :
        pos_num = 0
    elif  position == "정글" :
        pos_num = 1
    elif  position == "미드" :
        pos_num = 2
    elif  position == "원딜" :
        pos_num = 3
    elif  position == "서폿" :
        pos_num = 4

    ret = game.set_team_master(id, team1_master, team2_master, pos_num)
    if ret[0] == False:
        await ctx.send(ret[1])
    else:
        await ctx.send(ret[1])
        await ctx.send(game.draft()[1])

@bot.command()
async def 픽(ctx, text = None):
    if text is None:
        help_str = ''
        help_str += '!픽 매물번호 포지션(탑/정글/미드/원딜/서폿)\n'
        help_str += 'ex) !픽 1 탑'
        embed = discord.Embed(title="도움말", description=help_str, color=0x62c1cc)
        await ctx.send(embed=embed)
        return

    global game

    id = ctx.author.id

    strings = text.split()
    pick = int(strings[0])
    position = strings[1]
    pos_num = 0
    if position == "탑" :
        pos_num = 0
    elif  position == "정글" :
        pos_num = 1
    elif  position == "미드" :
        pos_num = 2
    elif  position == "원딜" :
        pos_num = 3
    elif  position == "서폿" :
        pos_num = 4

    ret = game.set_pick(id, pick, pos_num)
    if ret[0] == False:
        await ctx.send(ret[1])
    else:
        await ctx.send(ret[1])
        await ctx.send(game.draft()[1])

@bot.command()
async def 팀(ctx):
    global game

    embed = discord.Embed(title="팀 정보", description="", color=0x62c1cc)
    team1_info = "{} : {} \n".format(T, game.team1.member[0].discord_name  if type(game.team1.member[0]) == User else "")
    team1_info += "{} : {} \n".format(J,game.team1.member[1].discord_name  if type(game.team1.member[1]) == User else "")
    team1_info += "{} : {} \n".format(M,game.team1.member[2].discord_name  if type(game.team1.member[2]) == User else "")
    team1_info += "{} : {} \n".format(A,game.team1.member[3].discord_name  if type(game.team1.member[3]) == User else "")
    team1_info += "{} : {}   ".format(S,game.team1.member[4].discord_name  if type(game.team1.member[4]) == User else "")
    team2_info = "{} : {} \n".format(T, game.team2.member[0].discord_name  if type(game.team2.member[0]) == User else "")
    team2_info += "{} : {} \n".format(J,game.team2.member[1].discord_name  if type(game.team2.member[1]) == User else "")
    team2_info += "{} : {} \n".format(M,game.team2.member[2].discord_name  if type(game.team2.member[2]) == User else "")
    team2_info += "{} : {} \n".format(A,game.team2.member[3].discord_name  if type(game.team2.member[3]) == User else "")
    team2_info += "{} : {}   ".format(S,game.team2.member[4].discord_name  if type(game.team2.member[4]) == User else "")
    embed.add_field(name='1팀', value=team1_info, inline=True)
    embed.add_field(name='2팀', value=team2_info, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def 승리(ctx, text = None):
    if text is None:
        help_str = ''
        help_str += '!승리 팀(1팀/2팀)\n'
        help_str += 'ex) !승리 1팀'
        embed = discord.Embed(title="도움말", description=help_str, color=0x62c1cc)
        await ctx.send(embed=embed)
        return

    global game

    id = ctx.author.id

    ret = game.win(id, text)
    await ctx.send(ret[1])

bot.run(os.environ['Token'])