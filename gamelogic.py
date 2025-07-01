import asyncio
import inspect
from server import Server
import commands
from classes import *
from classes import Player
from state import game
import db
#This dict comprehension generates the command dictionary from the command.py file
db = db.db()
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
    if player.bound["Status"] == True:
        reason = player.bound["Reason"]
        print(type(reason))
        allowed_cmds = game.allowed_cmd[reason]
        if cmd in allowed_cmds:
            result = await command(cmd,player,*args)
        else:
            result = {'message': "that command is not allowed right now."}
    else:
        result = await command(cmd,player,*args)
    print(f"Command Processor Result: {result=}")
    print(game.players)
    if isinstance(result,dict):
        scope = result.get("scope","player")
        message = result.get("message","") + '\n'
        if scope == "all":
            '''
            for p in allPlayers:
                try:
                    print(p.client)
                    await p.client.send(message)
                except Exception as e:
                    print(f"Error sending to {p.name}: {e}")
                    '''
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
    await client.send("welcome to the mud use login (username) (password) to login. Use createUser username password to create a new character")
    player = None
    while player is None:
        await client.send("\n>")
        data = await client.receive()
        command,*args = data.strip().split()
        if command == 'login':
            if len(args) == 2:
                username, password = args[0], args[1]
                where_clause=f"username = '{username}' AND password = '{password}'"
                if db.query('players',where_clause=where_clause) ==True:
                    player = Player(username,client)
            else: client.send("login failed")
        if command == 'createUser':
            if len(args) == 2:
                username, password = args[0],args[1]
                where_clause=f"username	= '{username}' AND password = '{password}'"
                if db.query('players',where_clause=where_clause) == False:
                    db.insert('players',['username','password'],[username,password])
                    player = Player(username,client)
                else: client.send('this user already exists')
            else: client.send('this needs 2 args')
    while True:
        await client.send(">")
        data = await client.receive()
        #if not data:
            #break
        if data.lower() in ('quit', 'exit'):      
            break
        await commandProcessor(data,player,game)
    print(f"{name} disconnected.")

async def main():
    server = Server('0.0.0.0', 1234, handle_client)
    await server.start()

    
if __name__ == '__main__':
    asyncio.run(main())

