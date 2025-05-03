from classes import *
from state import game
#print(id(game))
'''                                                                                                                                    
def [command](player, *args):                                                                                                          
    return {                                                                                                                           
        "scope": "",                                                                                                                
        "message": ""                                                                      
    }                                                                                                                                  
'''
def get_players(player):
     players = [p.name for p in game.players]     
     return "\n".join(players)

def whoami(player):
    return {
         'scope': 'player',
         'message': f'{player.name}'
         }
def clear(player):
   return "\033[2J\033[H"
def startGame(player):
     if game.status == 0:
          game.start()
          return {
               "scope": "all",
               "message": f"the game has started with {len(game.players)} players "
          }
     else:
          return {"scope": "player",
                  "message": "A game has already started."}
def roll(*player):
     dice = Dice()
     if game.state == "rolling for Turn Order":
          rolls = dice.roll(1)
          game.passroll(rolls,player)
     message = "you rolled a 6"
     return {"message" : "you rolled a six"}
