import os
import requests
import calendar
from datetime import datetime, timedelta #日付計算
from dotenv import load_dotenv #.envファイルを読み込む

#webhookのURLは秘密情報なのでコードに書かず、.env(GitHubに上げない)から読む
#このファイルと同じフォルダの.envを読む(どこから実行しても見つかるように)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
WEBHOOK = os.getenv("WEBHOOK_URL")
if not WEBHOOK:
    raise SystemExit(".envにWEBHOOK_URLがありません")

#Pythonは上から読むため、defは前に書く
def getDate():
    now = datetime.now() + timedelta(days=1)
    y,m = now.year,now.month

#   monthrange:⚪︎年⚪︎月の情報を返す。
# ①(5) → その月の1日が何曜日か（0=月曜, ..., 6=日曜）※今回は使わない
# ②(31)→ その月の最終日（何日まであるか）。8月なら31日
    _ , lastday = calendar.monthrange(y, m)

 # 月に日曜日が何日あるか
    c_sunday = sum(
        1 for d in range(1,lastday + 1) #range(1 to last(含まない))
            if datetime(y, m, d).weekday() == 6
            # sundays = sundays + 1　→ ⭐︎1⭐︎ for（内包表記)
    )
    if c_sunday == 5:
        weeks = 5
    else:
        weeks = 4

    #⇧三項演算子ver
    #     weeks =  5   if sundays == 5   else   4
    #    ［Trueの時］   ［条件］          ［Falseの時］
    return (now + timedelta(weeks=weeks)).strftime("%Y/%-m/%-d")

eve_date =(datetime.now() + timedelta(days=1) + timedelta(weeks=2)).strftime("%Y/%-m/%-d")
eve_date2 = getDate()

mes1 = f"""
　　 ･･━━･･━━･･━━･･━━･･
    実践進捗会 中間報告
    ･･━━･･━━･･━━･･━━･･
    ◎開催日：{eve_date}
    ◎時  間：19:30より
    ◎場  所：⁠💬(交流部屋)
    参加される方は✅リアクションお願いします！
    ━━┉┉┉┅
    ⚠️必読
    ━━┉┉┉┅
    ①リアクションが2つ以上ない場合は開催を見送ります。
    ②聞き専＆時間制限があっても参加できる方はリアクションお願いします。✅
    ⇩⇩⇩
        """

mes2 = f"""
　　 ･━━･･━━･･━━･･━━･･
       実践報告会
    ･･━━･･━━･･━━･･━━･･
    ◎開催日：{eve_date2}
    ◎時  間：19:30より
    ◎場  所：⁠💬(交流部屋)
    参加される方は✅リアクションお願いします！
    ━━┉┉┉┅
    ⚠️必読
    ━━┉┉┉┅
    ①リアクションが2つ以上ない場合は開催を見送ります。
    ②聞き専＆時間制限があっても参加できる方はリアクションお願いします。
        """

#content:決められたキー(本文)　Pythonの辞書:{}
res = requests.post(WEBHOOK,json={"content":mes1})
print("送信結果:", res.status_code)#成功したか専用数値(200とか)がでる
res2 = requests.post(WEBHOOK,json={"content":mes2})
print("送信結果:", res2.status_code)




# import os
# import discord
# from discord.ext import tasks #←拡張機能
# from datetime import datetime, timedelta #日付計算

# TOKEN = os.environ["D_BOT_TOKEN"]
# CH_ID = 1533305661415358726

# #インテント:イベントを受信(メッセージ送信、メンバーの入退出、リアクション等) 今回は送信のみ＝default
# intents = discord.Intents.default()
# client = discord.Client(intents = intents) #BOT本体のobj

# #[M1-1]
# @tasks.loop(hours=336) #2w = 14[日]*24[h]
# #関数（def）:何か待っている間はプログラム全体が完全に止まってしまう
# #async def :（非同期関数）は「待っている間、他の処理に切り替えられる」という特徴。
# async def send_messe():
#     ch = client.get_channel(CH_ID)
#     #strftime:指定した表示にさせる
#     eve_date = (datetime.now() + timedelta(weeks=4)).strftime("%Y/%-m/%-d")
#     # トリプルクォート（改行を含めてそのまま書ける）
#     message = f"""
#       メッセージ内容
#                """
#     await ch.send(message) 


# #[M1-2]Botがログインに成功した瞬間に、一度だけ実行される処理
# @client.event
# async def on_ready():
#     print(f"ログイン完了:{client.user}")
#     send_messe.start() #[M1-1]

# client.run(TOKEN)