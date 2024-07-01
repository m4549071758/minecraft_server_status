from mcstatus import JavaServer
import discord

intent = discord.Intents.default()

ADDRESS = "pechi.jp"
PORT = 25565

def server_info(ADDRESS, PORT):
    server = JavaServer(ADDRESS, PORT)

    status = server.status()

    version = status.version.name
    ping = status.latency
    players_online = status.players.online
    players_max = status.players.max

    return round(ping, 2), players_online, players_max, version

try:
    ping, players_online, players_max, version = server_info(ADDRESS, PORT)
    print(f"Minecraft サーバー {ADDRESS} の情報:")
    print(f"バージョン: {version}")
    print(f"Ping: {ping}ms")
    print(f"オンラインプレイヤー数: {players_online}/{players_max}")
except Exception as e:
    print("サーバーはオフラインです")

