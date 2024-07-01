from mcstatus import JavaServer
from datetime import datetime
import discord
import asyncio

ADDRESS = "SERVER_ADDRESS"
PORT = 25565
TOKEN = "YOUR_TOKEN"
CHANNEL_ID = YOUR_CHANNEL_ID
VERSION = "YOUR_VERSION"
status = ""

def server_info(ADDRESS, PORT):
    server = JavaServer(ADDRESS, PORT)

    status = server.status()

    ping = status.latency
    players_online = status.players.online
    players_max = status.players.max

    return round(ping, 2), players_online, players_max

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("logged in as " + client.user.name)
    print("------")

    # 10分ごとに、Minecraft サーバーの情報を取得しチャンネルにメッセージを送信する。
    while True:
        try:
            ping, players_online, players_max = server_info(ADDRESS, PORT)
            status = "オンライン"
        except:
            ping, players_online, players_max = "NaN ", "0 ", " 0"
            status = "オフライン"
        channel = client.get_channel(CHANNEL_ID)

        # チャンネルにメッセージが存在する場合、すべて削除する
        async for message in channel.history(limit=2):
            await message.delete()
        
        # メッセージを送信する
        await channel.send("```yaml\n"
                            f"サーバー: {ADDRESS}\n"
                            f"ステータス: {status}\n"
                            f"バージョン: {VERSION}\n"
                            f"プレイヤー: {players_online}/{players_max}\n"
                            f"ping: {ping}ms\n"
                            f"最終更新: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n"
                            "```")
        
        print(f"status: {status} | players: {players_online}/{players_max} | ping: {ping}ms | last update: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
        await asyncio.sleep(600)


client.run(TOKEN)