from tkinter import *
import socket
from time import *
from threading import *
#Name: Vinit Udasi
#Student:6847800
#Sub: COSC 2P13
class Game:
    def __init__(self,root):
        self.rows = 6
        self.cols = 7
        self.root = root
        self.defaultBg = "gray"
        self.titText = StringVar()
        self.titText.set("Waiting....")
        self.winnerText = StringVar()
        self.winnerText.set("")
        self.controls={}
        self.title=Label(self.root,textvariable=self.titText,width=10,height=1,bg='blue')
        self.title.grid(row=0,column=0,padx=2,pady=2,columnspan=3)
        self.sok = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sok.connect(("localhost",5555))
        thr = Thread(target = self.readBackGround)
        thr.daemon = True
        thr.start()
        self.plno = self.sok.recv(1024).decode()
        if self.plno == "1":
            self.bgColor = "red"
        elif self.plno == "2":
            self.bgColor = "yellow"
        for c in range(self.cols):
            self.addButton(1,c)
        for r in range(2,self.rows+2):
            for c in range(self.cols):
                self.addLabel(r,c)
        self.playerColor=Label(self.root,width=10,height=1,bg=self.bgColor)
        self.playerColor.grid(row=0,column=4,padx=2,pady=2)
        self.winnerInfo=Label(self.root,width=10,height=1,bg="gray",textvariable=self.winnerText)
        self.winnerInfo.grid(row=0,column=5,padx=2,pady=2)
        self.titText.set("Player : "+ self.plno)
    def addButton(self,r,c):
        b = Button(self.root,text=str(c+1),width=10,height=1,command=lambda:self.buttonClick(c))
        b.grid(row=r,column=c,padx=2,pady=2)
        self.controls[(r,c)]=b
    def addLabel(self,r,c,bgColor="gray"): #adding colour labels
        l = Label(self.root,width=10,height=1,bg=bgColor)
        l.grid(row=r,column=c,padx=2,pady=2)
        self.controls[(r,c)]=l
    def updateLabel(self,data):
        rows = data.split("\n")
        for rInd in range(len(rows)):
            cols = rows[rInd].split(" ")
            #print(cols)                        #updating colour lables after a player's turn.
            for cInd in range(len(cols)):
                if cols[cInd] == "1":
                    self.controls[(7-rInd,cInd)].configure(bg="red")
                elif cols[cInd] == "2":
                    self.controls[(7-rInd,cInd)].configure(bg="yellow")
    def resetLabel(self):
         for r in range(2,self.rows+2):
            for c in range(self.cols):  #reset the labels(pretty much a useless function as it is)
                self.controls[(r,c)].configure(bg="gray")
    def buttonClick(self,cpos):
        win = False
        #print(cpos)
        pos = str(cpos)
        self.sok.send(pos.encode())
        status = self.sok.recv(1024).decode()  #the win is set to be false by default and after checking the logic it will reset.
        s = status.split(":")
        if s[0] == "False":
            self.titText.set("No space available on "+str(pos)+", select position again:")
        elif s[0]== "Got Place":
            #print(s)
            data = ""
            data = self.sok.recv(1024).decode()
            #print(data)
            self.updateLabel(data)
        elif s[0]=="Winner":
            data = self.sok.recv(1024).decode()
            self.winnerText.set(s[1] + " Winner")
            #sleep(5)
            self.resetLabel()
            sleep(5)
            self.root.destroy()
        elif s[0] == "Game Tied":
            self.titText.set("Game Tied")
            sleep(2)
            self.root.destroy()
    def readBackGround(self):
        self.sok1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sok1.connect(("localhost",5556))
        while True:
##            status = self.sok1.recv(1024).decode()
##            s = status.split(":")
##            if s[0]=="Winner" and s[1] != self.plno:
            data = self.sok1.recv(1024).decode()
            print("winner: ",data, " : ",self.plno)
            if data != self.plno:
                self.winnerText.set(data + " Winner")
            #sleep(1)
                self.resetLabel()
                sleep(5)
                self.root.destroy()
root = Tk()
g = Game(root)                                            #Constructor call.

root.mainloop()



    

        
     


