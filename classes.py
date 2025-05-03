import asyncio
import random
import allowed
class Game:
    def __init__(self):
        self.players = []
        self.status = 0 
        self.state = ""
        self.turns= []
        self.rolls = {}
        self.allowed_cmd = {"roll for turn order":["roll"]

                      } 
    def add_player(self,player):
        self.players.append(player)
    def remove_player(self,player):
        if player in self.players:
            self.players.remove(player)
    def passroll(self,rolls,player):
        self.rolls[player] = rolls
    def get_all_players(self):
        return self.players
    def turnOrder(self):
        self.state ="rolling for turn order"
        reason = "roll for turn order"
        self.bind_players(reason)
        asyncio.create_task(self.broadcast('\r'+'please roll for turn order'+'\n'))
        
    def bind_player(self,player,reason):
        player.bound["Status"] = True
        player.bound["Reason"] = reason
        print(player.name)
    def bind_players(self,reason):
        for player in self.players:
            self.bind_player(player,reason)
    def start(self):
        self.status = 1
        self.turnOrder()
    async def broadcast(self,message):
        print("---broadcasting---")
        for player in self.players:
            await player.client.send(message)

class Player:
    Players = []
    def __init__(self,name,client):
        self.name = name
        self.client = client
        self.bound= {"Status": False, "Reason":""} 
class Dice:
    def __init__(self):
        self.rolls = []
        self.value = None
    def roll(self,quantity):
        self.rolls = {}
        for i in range(quantity):
            value= randint(1,6)
            self.rolls.append(value)
        self.rolls.sort(reverse=True)
        return self.rolls
