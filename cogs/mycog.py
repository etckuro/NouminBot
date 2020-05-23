from discord.ext import commands # Bot Commands Frameworkのインポート
import discord

import gspread # googleスプレッドシート用
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

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
            result = name + '...? 知らねっす！'
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
