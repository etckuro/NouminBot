from discord.ext import commands # Bot Commands Frameworkのインポート
import discord

import gspread # googleスプレッドシート用
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

import random

#google スプレッドシートのKEY
SPREADSHEET_KEY = ''

# コグとして用いるクラスを定義。
class MyCog(commands.Cog):

    #プレイヤーリスト
    playerList = pd.DataFrame()

    # MyCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.playerList = getPlayerList()   # プレイヤーリストを読み込む
         
    @commands.command()
    async def who(self, ctx, name):        
        result = ''
        if name in self.playerList.index:
            playerInfo = self.playerList.loc[name]
            for idx in playerInfo.index:
                result += idx + '： ' + playerInfo.at[idx] + '\n'
        else:
            result = name + '...? 知らない子ですね...'
        await ctx.send(result)

    @commands.command()
    async def reload(self, ctx, name):        
        result = 'プレイヤーリストを再読み込みしましたー！'
        self.playerList = getPlayerList()   # プレイヤーリストを読み込む
        await ctx.send(result)

    @commands.command()
    async def rate(self, ctx, strrate):        
        rate = int(float(strrate) * 10)
        result = ''
        successcount = 0
        failcount = 0
        maxfailcount = 0
        totalsuccesscount = 0
        for i in range(0, 100):
            for j in range(0, 10):
                if random.randrange(1000) in random.sample(range(1000), k=rate):
                    result += '@'
                    if maxfailcount < failcount:
                        maxfailcount = failcount
                    failcount = 0
                    successcount += 1
                    totalsuccesscount += 1
                else:
                    result += '+'
                    failcount += 1
            #print('%s %s/30' % (result, str(successcount).rjust(3,' ')))
            #result = ''
            successcount = 0
        #print('最大連続失敗回数： %d 回' % maxfailcount)  
        #print('成功回数： %d 回' % totalsuccesscount)  
        result = '最大連続失敗回数： ' + str(maxfailcount) + ' 回\n' + result
        result = '成功回数： ' + str(totalsuccesscount) + ' 回\n' + result
        result = '確率 ' + str(strrate) + ' % を1000回実行すると…\n' + result
        await ctx.send(result)

    #### メインとなるroleコマンド
    ###@commands.group()
    ###async def role(self, ctx):
    ###    # サブコマンドが指定されていない場合、メッセージを送信する。
    ###    if ctx.invoked_subcommand is None:
    ###        await ctx.send('このコマンドにはサブコマンドが必要です。')

    #### roleコマンドのサブコマンド
    #### 指定したユーザーに指定した役職を付与する。
    ###@role.command()
    ###async def add(self, ctx, member: discord.Member, role: discord.Role):
    ###    await member.add_roles(role)

    #### roleコマンドのサブコマンド
    #### 指定したユーザーから指定した役職を剥奪する。
    ###@role.command()
    ###async def remove(self, ctx, member: discord.Member, role: discord.Role):
    ###    await member.remove_roles(role)

    ###@commands.Cog.listener()
    ###async def on_message(self, message):
    ###    if message.author.bot:
    ###        return

    ###    if message.content == 'こんにちは':
    ###        await message.channel.send('こんにちは')

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(MyCog(bot)) # MyCogにBotを渡してインスタンス化し、Botにコグとして登録

# googleスプレッドからプレイヤーリスト読み込み
def getPlayerList():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('quick-doodad-277506-919b78e713ca.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_key(SPREADSHEET_KEY).sheet1
    data = wks.get_all_values()
    df = pd.DataFrame(data, columns=data[0]).set_index('名前',drop=False)   
    return df
