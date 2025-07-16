import asyncio
import inspect
from server import Server
import commands
from classes import *
from classes import Player
from state import game
import db
from loginManager import LoginManager
#This dict comprehension generates the command dictionary from the command.py file
db = db.db()
lm = LoginManager(db)
command_dict = {
    name: func
    for name, func in inspect.getmembers(commands, inspect.isfunction)
    }
async def command(cmd,player,*args):
    if cmd in command_dict:
        return command_dict[cmd](player,*args)
    else:
        return "That command is invalid\n"
async def commandProcessor(data,player,game):
    if data == "": data = "invalid" 
    cmd,*args = data.strip().split()
    result = await command(cmd,player,*args)
    print(f"Command Processor Result: {result=}")
    print(game.players)
    if isinstance(result,dict):
        scope = result.get("scope","player")
        message = result.get("message","") + '\n'
        if scope == "all":
            await game.broadcast(message)
        elif scope == "target":
            target_name = result.get("target")
            for p in allPlayers:
                if p.name == target_name:
                    await p.client.send(message)
                    break
        else:
            await player.client.send(message)
    else:
        print(player.client)
        print(player)
        await player.client.send(result)

async def handle_client(client):
    await client.send('\033[2J\033[H')
    await client.send("welcome to the mud use login (username) (password) to login. Use createUser username password to create a new character\n")
    player = None
    while player is None:
        try:
            await client.send(">")
            data = await client.receive()
            if not data: data = 'invalid'
            cmd, *args = data.strip().split()
            if len(args) == 2:
                username ,password = args[0],args[1]
                if cmd == 'login':
                   if await lm.login(username,password) == True: player = Player(username,client)
                   else: await client.send('that username or password is incorect')
                elif cmd == 'createUser':
                   if await lm.createPlayer(username,password) == True: player = Player(username,client)
                   else: await client.send('that username is not available')
            else:
                await client.send('this command requires 2 args')
        except ValueError as e:
           print('error')
    while True:
        try:
            await client.send(">")
            data = await client.receive()
            if not data: data = 'invalid'
                
            #break
            if data.lower() in ('quit', 'exit'):      
                break
            await commandProcessor(data,player,game)
        except ValueError as e:
            print('e')
            print(f"{username} disconnected.")
            break
async def main():
    server = Server('0.0.0.0', 1234, handle_client)
    await server.start()

    
if __name__ == '__main__':
    asyncio.run(main())

