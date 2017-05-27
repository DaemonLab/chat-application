#Developed By : Suryaveer from IIT INDORE
#UserName: @ayrusreev
#GitHub : http://www.github.com/surya-veer

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import socket 
import sys, socket, select
import time
from PyQt4.QtNetwork import *


SIZEOF_UINT32 = 4

class Chat(QDialog):
	#NOTE: Non-responsive layout 
	def __init__(self , parent = None):
		super(Chat,self).__init__(parent)
		layout = QHBoxLayout

		#initializing socket
		self.socket  = QTcpSocket()
		self.nextBlockSize = 0
		self.request = None


		self.setWindowTitle('Chat-Box')

		#height  = 500, width = 800
		self.setGeometry(300,100,800,500)

		#label 
		self.l1 = QLabel(self)
		self.l1.move(225,10)
		self.l1.setText('Chat-Box')
		self.l1.setFont(QFont("Arial",15))

		#char response text
		self.out = QTextBrowser(self)
		self.out.setGeometry(225,30,350,400)
		self.out.setText('<<welcome to my chat box>>')
		self.out.setFont(QFont("Arial",12))

		#send text-box(edit line)
		self.text = QLineEdit(self)
		self.text.setGeometry(225,435,350-40,40)
		self.text.setFont(QFont("Arial",12))
		self.text.setText("Type here")

		#send button
		self.sendBtn = QPushButton(self)
		self.sendBtn.setText('>>')
		self.sendBtn.setGeometry(225+350-40,435,42,40)
		self.sendBtn.clicked.connect(self.issueRequest)

		#online friends list
		self.l2 = QLabel(self)
		self.l2.move(225+360,10)
		self.l2.setText('Online Friends')
		self.l2.setFont(QFont("Arial",15))

		self.friendList = QListWidget (self)
		self.friendList.setGeometry(225+360,30,200,400)
		self.friendList.insertItem (0, 'Ankit' )
		self.friendList.insertItem (1, 'Mohit' )
		self.friendList.insertItem (2, 'Kailash' )
		self.friendList.insertItem (3, 'Sanchit' )
		self.friendList.insertItem (4, 'Aditya' )
		self.friendList.insertItem (5, 'Vineet' )

		self.offlineBtn = QPushButton(self)
		self.offlineBtn.setText('Go Offline')
		self.offlineBtn.setGeometry(225+360+100,435,100,40)

		self.refreshBtn = QPushButton(self)
		self.refreshBtn.setText('Refresh')
		self.refreshBtn.setGeometry(225+360,435,100,40)
		self.refreshBtn.clicked.connect(self.Refresh)

		#settings section
		self.l3 = QLabel(self)
		self.l3.move(80,10)
		self.l3.setText('Settings')
		self.l3.setFont(QFont("Arial",15))

		#ip address
		self.l4 = QLabel(self)
		self.l4.move(10,40)
		self.l4.setText('IP Address')
		self.l4.setFont(QFont("Arial",12))

		self.ip = QLineEdit(self)
		self.ip.setGeometry(10,55,130,30)
		self.ip.setFont(QFont("Arial",12))
		self.ip.setText("127.0.0.1")

		#port no.
		self.l5 = QLabel(self)
		self.l5.move(150,40)
		self.l5.setText('Port')
		self.l5.setFont(QFont("Arial",12))

		self.port = QLineEdit(self)
		self.port.setGeometry(150,55,60,30)
		self.port.setFont(QFont("Arial",12))
		self.port.setText("8888")

		#Nick name
		self.l4 = QLabel(self)
		self.l4.move(10,110)
		self.l4.setText('UserName')
		self.l4.setFont(QFont("Arial",12))

		self.userName = QLineEdit(self)
		self.userName.setGeometry(10,130,200,30)
		self.userName.setFont(QFont("Arial",12))
		self.userName.setText("Ayrus")

		#connect button
		self.connectBtn = QPushButton(self)
		self.connectBtn.setText('Connect')
		self.connectBtn.setGeometry(10,180,200,30)
		self.connectBtn.setEnabled(True)

		#disconnect button
		self.disconnectBtn = QPushButton(self)
		self.disconnectBtn.setText('Disconnect')
		self.disconnectBtn.setGeometry(10,220,200,30)
		self.disconnectBtn.setEnabled(False)
		self.disconnectBtn.clicked.connect(self.Disconnect)

		#status
		self.l5 = QLabel(self)
		self.l5.move(80,300)
		self.l5.setText('Status')
		self.l5.setFont(QFont("Arial",15))

		self.l6 = QLabel(self)
		self.l6.setFont(QFont("Arial",20))
		self.statusColor(0)
		self.l6.setText('Disconnected')

		
		

		#how to use
		self.howBtn = QPushButton(self)
		self.howBtn.setText('how to use?')
		self.howBtn.setGeometry(10,400,200,30)
		self.howBtn.clicked.connect(self.howToUse)

		#about
		self.aboutBtn = QPushButton(self)
		self.aboutBtn.setText('About')
		self.aboutBtn.setGeometry(10,445,200,30)

		self.aboutBtn.clicked.connect(self.about)



		self.text.returnPressed.connect(self.issueRequest)
		self.connectBtn.clicked.connect(self.connect)

		#read from server
		self.socket.readyRead.connect(self.readFromServer)



	def statusColor(self,status):
		palette = QPalette()
		if status:
			c=QColor(0,225, 0,225)
			self.l6.move(50,330)
		else:
			c=QColor(255,0, 0,255)
			self.l6.move(40,330)

		palette.setColor(QPalette.Foreground,c)
		self.l6.setPalette(palette)


	def howToUse(self):
		self.msg=QMessageBox()
		self.msg.setIcon(QMessageBox.Information)
		self.msg.setText("How to use?")
		self.msg.setInformativeText("Click on show details..")
		self.msg.setWindowTitle("How to use?")
		self.msg.setDetailedText("The details are as follows:")
		self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		self.retval=self.msg.exec_()



	def about(self):
		self.msg=QMessageBox()
		self.msg.setIcon(QMessageBox.Information)
		self.msg.setText("This is a simple chat-box")
		self.msg.setInformativeText("Developed By: Suryaveer")
		self.msg.setWindowTitle("About")
		self.msg.setDetailedText("Developed By: Suryaveer\nEmail: 1998sveer@gmil.com\n")
		self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		self.retval=self.msg.exec_()
		


	def connect(self):
		self.socket.connectToHost(self.ip.text(),int(self.port.text()))
		self.connectBtn.setEnabled(False)
		self.disconnectBtn.setEnabled(True)
		self.text.setEnabled(True)
		self.userName.setEnabled(False)
		self.text.setFocus()
		self.statusColor(1)
		self.l6.setText("Connected")


	def issueRequest(self):
		if self.text.text():
			self.request = QByteArray()
			stream = QDataStream(self.request,QIODevice.WriteOnly)
			stream.setVersion(QDataStream.Qt_4_2)
			stream.writeUInt32(0)
			stream.writeQString('<' + self.userName.text()+'>: '+self.text.text())
			stream.device().seek(0)
			stream.writeUInt32(self.request.size() - SIZEOF_UINT32)
			self.socket.write(self.request)
			self.nextBlockSize = 0
			self.request = None
			self.text.setText("")


	def readFromServer(self):
		stream = QDataStream(self.socket)
		stream.setVersion(QDataStream.Qt_4_2)
		while 1:
			if self.nextBlockSize == 0:
				if self.socket.bytesAvailable() < SIZEOF_UINT32:
					break
				self.nextBlockSize = stream.readUInt32()
			if self.socket.bytesAvailable() < self.nextBlockSize:
				break
			textReceive = stream.readQString()
			self.update(textReceive)
			self.nextBlockSize = 0

	def update(self,text):
		self.out.append(text)


	def Disconnect(self):
		self.socket.close()
		self.disconnectBtn.setEnabled(False)
		self.connectBtn.setEnabled(True)
		self.text.setEnabled(False)
		# self.userName.setEnabled(True)
		self.connectBtn.setFocus()
		self.statusColor(0)
		self.l6.setText("Disconnected")


	def Refresh(self):
		self.out.setText("<<welcome to my chat box>>")
	 
def main():
	app = QApplication(sys.argv)
	ex = Chat()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()