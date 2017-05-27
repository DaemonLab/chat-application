#Developed By : Suryaveer from IIT INDORE
#UserName: @ayrusreev
#GitHub : http://www.github.com/surya-veer

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

SIZEOF_UINT32 = 4

class ChatServer(QDialog):

    def __init__(self, parent=None):
        super(ChatServer,self).__init__(parent)
        layout = QHBoxLayout
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
	
        #height  = 500, width = 800
        self.setGeometry(300,100,300,300)

        #label 
        self.l1 = QLabel(self)
        self.l1.move(40+10,20)
        self.l1.setText('Chat Server')
        self.l1.setFont(QFont("Arial",30))

        self.l2 = QLabel(self)
        self.l2.move(45+10,100)
        self.l2.setText('Is running on: localhost')
        self.l2.setFont(QFont("Arial",15))

        self.l2 = QLabel(self)
        self.l2.move(90+10,150)
        self.l2.setText('Port No: 8888')
        self.l2.setFont(QFont("Arial",15))

        self.exitBtn = QPushButton(self)
        self.exitBtn.setText('Stop Server')
        self.exitBtn.setGeometry(65+10,200,160,40)
        self.exitBtn.setFont(QFont("Arial",20))
        self.exitBtn.clicked.connect(self.StopServer)



        #creating server
        self.tcpServer = QTcpServer(self)               
        self.tcpServer.listen(QHostAddress("0.0.0.0"), 8888)
        self.connect(self.tcpServer, SIGNAL("newConnection()"), 
                    self.add)
        self.connections = []
        
        self.setWindowTitle("Chat Server")


    def StopServer(self):
        quit()


    def add(self):
        clientConnection = self.tcpServer.nextPendingConnection()
        clientConnection.nextBlockSize = 0
        self.connections.append(clientConnection)

        self.connect(clientConnection, SIGNAL("readyRead()"), 
                self.receiveData)
 

    def receiveData(self):
        for s in self.connections:
            if s.bytesAvailable() > 0:
                stream = QDataStream(s)
                stream.setVersion(QDataStream.Qt_4_2)

                if s.nextBlockSize == 0:
                    if s.bytesAvailable() < SIZEOF_UINT32:
                        return
                    s.nextBlockSize = stream.readUInt32()
                if s.bytesAvailable() < s.nextBlockSize:
                    return

                textFromClient = stream.readQString()
                s.nextBlockSize = 0
                self.sendData(textFromClient, 
                                 s.socketDescriptor())
                s.nextBlockSize = 0

    def sendData(self, text, socketId):
        for s in self.connections:
            if s.socketDescriptor() == socketId:
		pre, post = text.split(">:")
                message = "\n<[Me]> {}".format(post)
		print message
            else:
                message = "\n {}".format(text)
            reply = QByteArray()
            stream = QDataStream(reply, QIODevice.WriteOnly)
            stream.setVersion(QDataStream.Qt_4_2)
            stream.writeUInt32(0)
            stream.writeQString(message)
            stream.device().seek(0)
            stream.writeUInt32(reply.size() - SIZEOF_UINT32)
            s.write(reply)


def main():
    app = QApplication(sys.argv)
    form = ChatServer()
    form.show()
    form.move(650,460)
    app.exec_()
    
if __name__ == '__main__':
    main()
