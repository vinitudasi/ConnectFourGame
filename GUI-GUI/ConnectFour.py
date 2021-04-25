from threading import *
#Name: Vinit Udasi
#Student:6847800
#Sub: COSC 2P13
class ConnectFour:
    def __init__(self): #Game Logic implemented in this class.
        self.cols = 7
        self.rows = 6
        self.playGround = [['b' for _ in range(self.cols)]for _ in range(self.rows)]
        self.l = Lock()
        self.active = True
        self.plyOne = True
        self.plyTwo = False
        self.winner = False
        self.winName=""
    def clearPlayGround(self):
        self.playGround = [['b' for _ in range(self.cols)]for _ in range(self.rows)] #clear the playground.
    def printPlayGround(self):
        for r in range(self.rows):
            print(*(self.playGround[r])) #Printing the ground.
    def setValue(self,marker,cPos):
        self.l.acquire()
        for r in range(self.rows):
            if self.playGround[r][cPos] == "b":
                self.playGround[r][cPos] = marker
                win = self.checkWinner(marker,cPos,r)
                self.l.release()
                return (True,win,r)
        self.l.release()
        return (False,)
        
    def checkWinner(self,marker,cpos,rpos): #Checks the winner after a bunch of inputs
        count = 0
        tcol = cpos
        while tcol < self.cols and count<4:
            if self.playGround[rpos][tcol] == marker:
                count+=1
                tcol+=1
                continue
            break
        if count ==4 :
            return marker
        tcol = cpos-1
        while tcol >= 0 and count<4:
            if self.playGround[rpos][tcol] == marker:
                count+=1
                tcol-=1
                continue
            break
        if count ==4 :
            return marker
        trow = rpos
        count = 0
        while trow< self.rows and count <4:
            if self.playGround[trow][cpos] == marker:
                count+=1
                trow+=1
                continue
            break
        if count == 4:
            return marker
        trow = rpos-1
        while trow >=0 and count<4:
            if self.playGround[trow][cpos] == marker:
                count+=1
                trow-=1
                continue
            break
        if count == 4:
            return marker
        count  = 0
        if self.playGround[rpos][cpos] == marker:
            count+=1
            trow = rpos-1;tcol=cpos+1
            while trow>=0 and tcol<self.cols and count <4:
                if self.playGround[trow][tcol] == marker:
                    trow-=1
                    tcol+=1
                    count+=1
                    continue
                break
            if count ==4 :
                return marker
            trow = rpos+1;tcol=cpos-1
            while trow < self.rows and tcol>=0 and count<4:
                if self.playGround[trow][tcol] == marker:
                    trow +=1
                    tcol-=1
                    count+1
                    continue
                break
            if count ==4:
                return marker
            trow = rpos-1;tcol=cpos-1;count=1
            while trow>=0 and tcol>=0 and count <4:
                if self.playGround[trow][tcol] == marker:
                    trow-=1
                    tcol-=1
                    count+=1
                    continue
                break
            if count ==4 :
                return marker
            trow = rpos+1;tcol=cpos+1
            while trow<self.rows and tcol < self.cols and count < 4:
                if self.playGround[trow][tcol] == marker:
                    trow+=1
                    tcol+=1
                    count+=1
                    continue
                break
            if count == 4:
                return marker
        return "0"
