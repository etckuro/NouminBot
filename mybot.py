from discord.ext import commands # Bot Commands Frameworkをインポート
import traceback # エラー表示のためにインポート

#BOTのトークン
TOKEN = ''

# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.mycog'
]

# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class MyBot(commands.Bot):

    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print(self.user.name + ' 開始!!')
        print(self.user.id)

# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    bot = MyBot(command_prefix='/') # command_prefixはコマンドの最初の文字として使うもの。
    bot.run(TOKEN) # Botのトークン
