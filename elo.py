#ELO
#python 3.4.3
import math

class ELOPlayer:
    name      = ""
    place     = 0
    eloPre    = 0
    eloPost   = 0
    eloChange = 0
    
class ELOMatch:
    def __init__(self):
        self.players = []
        self.knum = 32
        self.preround = True
        self.changemult = 1
    
    def setKnum(self, knum):
        if knum > 0:
            self.knum = knum
        else:
            print("knum <=0 is invalid, keeping old value")

    def setPreround(self, preround):
        self.preround = preround

    def setChangeMultiplier(self, changemult):
        self.changemult = changemult

    def addPlayer(self, name, place, elo):
        player = ELOPlayer()
        
        player.name    = name
        player.place   = place
        player.eloPre  = elo
        
        self.players.append(player)
        
    def getELO(self, name):
        for p in self.players:
            if p.name == name:
                return p.eloPost
            
        return 1500

    def getELOChange(self, name):
        for p in self.players:
            if p.name == name:
                return p.eloChange
                
        return 0
 
    def calculateELOs(self):
        n = len(self.players)
        K = self.knum / (n - 1)
        for player in self.players:
            curPlace = player.place
            curELO   = player.eloPre

            for opponent in self.players:
                if player == opponent:
                    continue
                
                opponentPlace = opponent.place
                opponentELO   = opponent.eloPre  
                
                #work out S
                if curPlace < opponentPlace:
                    S = 1.0
                elif curPlace == opponentPlace:
                    S = 0.5
                else:
                    S = 0.0
                
                #work out EA
                EA = 1 / (1.0 + math.pow(10.0, (opponentELO - curELO) / 400.0))
                
                #calculate ELO change vs this one opponent, add it to our change bucket
                #I currently round at this point, this keeps rounding changes symetrical between EA and EB, but changes K more than it should
                if self.preround:
                    player.eloChange += round(self.changemult * K * (S - EA))
                else:
                    player.eloChange += self.changemult * K * (S - EA)

            #add accumulated change to initial ELO for final ELO   
            if self.preround:
                player.eloPost = player.eloPre + player.eloChange
            else:
                player.eloPost = player.eloPre + round(player.eloChange)
