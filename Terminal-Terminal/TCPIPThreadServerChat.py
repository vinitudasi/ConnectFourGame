from time import *
from threading import *
from socket import *
from ConnectFour import ConnectFour
class ThreadServer:
    def __init__(self,client,addr,marker):
        self.client=client
        self.addr = addr
        self.marker = marker
    def setMarker(self,marker):
        self.marker = marker
    def start(self,objCon):
        self.client.send(self.marker.encode())
        con=True
        r = 0
        while(current_thread().getName() == "Thread-1" and objCon.plyTwo == True):
                sleep(1.0)
        while(current_thread().getName() == "Thread-2" and objCon.plyOne == True):
                sleep(1.0)
        while con:
            while(current_thread().getName() == "Thread-1" and objCon.plyTwo == True):
                sleep(1.0)
            while(current_thread().getName() == "Thread-2" and objCon.plyOne == True):
                sleep(1.0)
            while r < 6 :
                while(current_thread().getName() == "Thread-1" and objCon.plyTwo == True):
                    sleep(1.0)
                while(current_thread().getName() == "Thread-2" and objCon.plyOne == True):
                    sleep(1.0)
                pos = self.client.recv(1024).decode()
                print(self.marker ,': Position:  ', pos)
                status = objCon.setValue(self.marker,int(pos))
                if len(status) ==1:
                    r+=1
                    self.client.send("False:".encode())
                    pos = self.client.recv(1024)
                    status = objCon.setValue(self.marker,int(pos))
                    print(status)
                    if r ==5 and len(status) == 1:
                        self.client.send("No Position:".encode())
                        con = False
                    elif len(status) == 3:
                        if status[1] == "0":
                            self.client.send(("Got Place:"+str(status[2])).encode())
                            data=""
                            for each in objCon.playGround:
                                data += " ".join(each) + "\n"
                            self.client.send(data.encode())
                            if current_thread().getName() == "Thread-1":
                                objCon.plyOne = False
                                objCon.plyTwo = True
                                break
                            elif current_thread().getName()=="Thread-2":
                                objCon.plyTwo = False
                                objCon.plyOne = True
                                break
                        elif status[1] == self.marker:
                            print(self.marker, " Winner")
                            self.client.send(("Winner:"+self.marker).encode())
                            objCon.winner = status[1]
                            for each in objCon.playGround:
                                data += " ".join(each) + "\n"
                            self.client.send(data.encode())
                            objCon.winner = True
                            objCon.winnerName = self.marker
                            con = False
                        break
                elif len(status)==3:
                    if status[1] == "0":
                        self.client.send(("Got Place:"+str(status[2])).encode())
                        data=""
                        for each in objCon.playGround:
                            data += " ".join(each) + "\n"
                        self.client.send(data.encode())
                        if current_thread().getName() == "Thread-1":
                            objCon.plyOne = False
                            objCon.plyTwo = True
                            objCon.printPlayGround()
                            break
                        elif current_thread().getName()=="Thread-2":
                            objCon.plyTwo = False
                            objCon.plyOne = True
                            objCon.printPlayGround()
                            break
                    elif status[1] == self.marker:
                        print(self.marker, " Winner")
                        self.client.send(("Winner:"+self.marker).encode())
                        for each in objCon.playGround:
                            data += " ".join(each) + "\n"
                        self.client.send(data.encode())
                        objCon.winner = True
                        objCon.winnerName = self.marker
                        objCon.printPlayGround()
                    break
            if objCon.winner == True:
                name = current_thread().getName()
                print("Thread Name : " + name)
                print("Winner Name: " ,objCon.winnerName ," "  , name.split("-"))
                if name == "Thread-1" and objCon.winnerName != name.split("-")[1]:
                    self.client.send(("Winner:"+objCon.winnerName).encode())
                    objCon.winner = False
                    objCon.plyTwo = False
                    objCon.plyOne = True
                    objCon.clearPlayGround()
                    objCon.winnerName =""
                    for each in objCon.playGround:
                            data += " ".join(each) + "\n"
                    self.client.send(data.encode())
                elif name == "Thread-2" and objCon.winnerName != name.split("-")[1]:
                    self.client.send(("Winner:"+objCon.winnerName).encode())
                    objCon.winner = False
                    objCon.plyTwo = False
                    objCon.plyOne = True
                    objCon.clearPlayGround()
                    objCon.winnerName =""
                    for each in objCon.playGround:
                            data += " ".join(each) + "\n"
                    self.client.send(data.encode())
            if con == False:
                self.client.send(str("Game over  No one is won:").encode())
                objCon.winner = False
                objCon.plyTwo = False
                objCon.plyOne = True
                objCon.clearPlayGround()
                objCon.winnerName =""
                

host = "localhost"
port =5555
sok =socket()
sok.bind((host,port))
sok.listen(2)
print("server start")
conFour = ConnectFour()
marker = 0
lstThread=[]
clients=[]
while True:
    client,addr = sok.accept()
    print(' Request accept from client address ', str(addr))
    marker+=1
    ser = ThreadServer(client,addr,str(marker))
    clients.append(ser)
    thred= Thread(target=ser.start,args=(conFour,))
    thred.setName("Thread-"+str(marker))
    thred.daemon=True
    #thred.start()
    lstThread.append(thred)
    if marker == 2:
        lstThread[0].start()
        lstThread[1].start()
##while True:
##    if conFour.winner == True:
####        while lstThread[0].is_alive() or lstThread[1].is_alive():
####            sleep(1)
##        if conFour.winnerName == "1":
##            lstThread[0].join()
##        else:
##            lstThread[1].join()
##        clients[0],clients[1] = clients[0],clients[1]
##        thred1= Thread(target=clients[0].start,args=(conFour,))
##        thred2= Thread(target=clients[1].start,args=(conFour,))
##        #objThread1,objThread2 = lstThread[1],lstThread[0]
##        thred1.setName("Thread-1")
##        thred2.setName("Thread-2")
##        lstThread.clear()
##        lstThread.append(thred1)
##        lstThread.append(thred2)
##        conFour.winner = False
##        conFour.plyOne = True
##        conFour.playTwo = False
##        thred1.start()
##        thred2.start()
        
