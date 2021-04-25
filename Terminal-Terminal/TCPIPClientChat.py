import socket
#Name: Vinit Udasi
#Student:6847800
#Sub: COSC 2P13
class Game:
    def __init__(self):
        self.cols = 7
        self.rows = 6
        self.playGround = [['b' for _ in range(self.cols)]for _ in range(self.rows)]
    def printPlayGround(self):
        for r in range(self.rows):
            print(*(self.playGround[r]))
    def setValue(self,marker,r,cPos):
        self.playGround[r][cPos] = marker

host='localhost'
port = 5555
sok = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sok.connect((host,port))
plno = sok.recv(1024).decode()
print("Player No: ",plno)
con = True
g = Game()
win = False
while con:
    for r in range(6):
        pos = input("Enter position: ")
        sok.send(pos.encode())
        status = sok.recv(1024).decode()
        s = status.split(":")
        if s[0] == "False":
            pos = input("No space available on "+str(pos)+", Enter position again(player 1): ")
            sok.send(pos.encode())
            status = sok.recv(1024).decode()
            #status = c.setValue("1",pos)
            s = status.split(":")
            if r == 5 and s[0]== "False":
                print ("No position available :")
                con = False
                break
            elif s[0]== "Got Place":
                data = ""
                data = sok.recv(1024).decode()
                print(data)
                break
            elif s[0] == "Winner":
                print(s[1] + " Winner: ")
                win = True
                con = False
                break
        elif s[0]== "Got Place":
            print(s)
            data = ""
            data = sok.recv(1024).decode()
            print(data)   
            break
        elif s[0]=="Winner":
            print(s[1] +  " Winner")
            win = True
            break
    if win == True:
        print("Game restart")
        win = False
    if con == False:
        con=True
        print("Game over: No one is win")
        
##    msg = input("Enter msg: ")
##    sok.send(msg.encode())
##    msg = sok.recv(1024).decode()
##    print("Server: ",msg)
##    msg = input("Enter Message for server: ")
sok.close()
