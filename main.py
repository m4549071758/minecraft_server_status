from mcstatus import JavaServer
import discord
import asyncio

ADDRESS = "pechi.jp"
PORT = 25565
TOKEN = "YOUR_DISCORD_TOKEN"
CHANNEL_ID = 1257251108787589161

def server_info(ADDRESS, PORT):
    server = JavaServer(ADDRESS, PORT)

    status = server.status()

    version = status.version.name
    ping = status.latency
    players_online = status.players.online
    players_max = status.players.max

    return round(ping, 2), players_online, players_max, version

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("logged in as " + client.user.name)
    print("------")

    # 10分ごとに、Minecraft サーバーの情報を取得しチャンネルにメッセージを送信する。
    # メッセージを送信する場合、チャンネルに1つ以上メッセージが存在する場合は、そのメッセージを編集する形式にする。
    while True:
        try:
            ping, players_online, players_max, version = server_info(ADDRESS, PORT)
            channel = client.get_channel(CHANNEL_ID)
            messages = await channel.history(limit=1).flatten()
            if len(messages) == 0:
                await channel.send(f"Minecraft サーバー {ADDRESS} の情報:")
                await channel.send(f"バージョン: {version}")
                await channel.send(f"Ping: {ping}ms")
                await channel.send(f"オンラインプレイヤー数: {players_online}/{players_max}")
            else:
                await messages[0].edit(content=f"Minecraft サーバー {ADDRESS} の情報:")
                await messages[1].edit(content=f"バージョン: {version}")
                await messages[2].edit(content=f"Ping: {ping}ms")
                await messages[3].edit(content=f"オンラインプレイヤー数: {players_online}/{players_max}")
        except Exception:
            channel = client.get_channel(CHANNEL_ID)
            messages = await channel.history(limit=1).flatten()
            if len(messages) == 0:
                await channel.send("サーバーはオフラインです")
            else:
                await messages[0].edit(content="サーバーはオフラインです")
        await asyncio.sleep(600)

client.run(TOKEN)