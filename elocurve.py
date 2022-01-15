#ELO
#python 3.4.3
import math
from scipy import asarray as ar
from scipy.stats import skewnorm
import datetime
import time

class ELOPlayer:
    name      = ""
    time      = 0
    eloPre    = 0
    eloPost   = 0
    eloChange = 0
    
class ELOMatch:
    def __init__(self):
        self.players = []
        self.knum = 32
        self.preround = True
        self.changemult = 1
        self.fit_curve = None
    
    def setKnum(self, knum):
        if knum > 0:
            self.knum = knum
        else:
            print("knum <=0 is invalid, keeping old value")

    def setPreround(self, preround):
        self.preround = preround

    def setChangeMultiplier(self, changemult):
        self.changemult = changemult

    def addPlayer(self, name, ptime, elo):
        player = ELOPlayer()
        
        player.name    = name
        if isinstance(ptime, str):
            t = time.strptime(ptime, '%H:%M:%S')
            player.time = datetime.timedelta(hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec).total_seconds()
        else:
            player.time = ptime
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

    def calculateCurve(self):
        ts_arr = ar([p.time for p in self.players if p.time > 0])
        self.fit_curve = skewnorm(*skewnorm.fit(ts_arr))
 
    def calculateELOs(self):
        if self.fit_curve is None:
            self.calculateCurve()
        n = len(self.players)
        K = self.knum / (n - 1)
        for player in self.players:
            #curPlace = player.place
            curTime = player.time
            if curTime > 0 :
                curSF = self.fit_curve.sf(curTime)
            else:
                curSF = 0
            curELO   = player.eloPre

            for opponent in self.players:
                if player == opponent:
                    continue
                
                #opponentPlace = opponent.place
                opponentTime = opponent.time
                if opponentTime > 0:
                    opSF = self.fit_curve.sf(opponentTime)
                else:
                    opSF = 0
                opponentELO   = opponent.eloPre  
                
                # both SF values are between 0 and 1, with 1 being better. wins should end up in 0.5-1, while losses should end up in 0-0.5. So, we take the difference between the SFs, divide by 2, and add that to 0.5
                sfdiff = curSF - opSF # this will be between 1 and -1, positive for wins and negative for losses
                S = 0.5 + (sfdiff / 2)

                #work out S
                #if curPlace < opponentPlace:
                #    S = 1.0
                #elif curPlace == opponentPlace:
                #    S = 0.5
                #else:
                #    S = 0.0
                
                #work out EA
                EA = 1 / (1.0 + math.pow(10.0, (opponentELO - curELO) / 400.0))
                #print(player.name, opponent.name, S, EA)
                
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
