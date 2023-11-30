#KN: Interface handling

from rec import Recorder
from tkinter import *
import threading
import time
import os

class Screen():

	def __init__(self, mode):
		# Control flags
		self.modep = mode     # int number 1: Debug Mode, 2: Verbose Mode, 3: Normal Mode
		# Flags
		self.arrows = 1     # Arrows disable/enable
		self.user_type = 0     # 0=Id / 1=Des
		self.c_joystick = 0
		self.it = 0
		self.sec = 0
		self.path = os.getcwd()
		self.interface()

	def interface(self):
		self.root = Tk()
		self.root.title("Audio Recorder")
		self.root.iconbitmap(self.path + "/Img/grc.ico")
		self.root.resizable(0,0)
		self.window = Frame(self.root, width=480, height=295)
		self.window.pack()
		self.i_userId = PhotoImage(file=self.path + "/Img/id.png")
		self.userId = Label(self.window, image=self.i_userId)
		self.userId.grid(row=0, column=1, padx=10, pady=10, rowspan=2, columnspan=2)
		self.userId.bind("<Button-1>", self.chosenID)
		self.i_userDes = PhotoImage(file=self.path + "/Img/des0.png")
		self.userDes = Label(self.window, image=self.i_userDes)
		self.userDes.grid(row=0, column=3, padx=10, pady=10, rowspan=2, columnspan=2)
		self.userDes.bind("<Button-1>", self.chosenDes)
		# Buttons
		self.i_upButton = PhotoImage(file=self.path + "/Img/up.png")
		self.upButton = Button(self.window, image=self.i_upButton, command=self.up)
		self.upButton.grid(row=0, column=0, sticky="s", padx=10, pady=7)
		self.i_downButton = PhotoImage(file=self.path + "/Img/down.png")
		self.downButton = Button(self.window, image=self.i_downButton, command=self.down)
		self.downButton.grid(row=1, column=0, sticky="n", padx=10, pady=7)
		self.time = Label(self.window, fg="green", width=2, text="00", bg="gainsboro", font=("", "22"), state=DISABLED)
		self.time.place(x=13, y=170)
		self.i_resetButton = PhotoImage(file=self.path + "/Img/reset.png")
		self.resetButton = Button(self.window, image=self.i_resetButton, command=self.reset, state=DISABLED)
		self.resetButton.grid(row=2, column=0)
		self.i_speakButton = PhotoImage(file=self.path + "/Img/speak.png")
		self.speakButton = Button(self.window, image=self.i_speakButton, command=self.record, state=DISABLED)
		self.speakButton.grid(row=2, column=1)
		self.i_stotButton = PhotoImage(file=self.path + "/Img/stop_speak.png")
		self.stopButton = Button(self.window, image=self.i_stotButton, command=self.stop, state=DISABLED)
		self.stopButton.grid(row=2, column=2)
		self.i_playButton = PhotoImage(file=self.path + "/Img/play.png")
		self.playButton = Button(self.window, image=self.i_playButton, command=self.play, state=DISABLED)
		self.playButton.grid(row=2, column=3)
		self.i_sendButton = PhotoImage(file=self.path + "/Img/send.png")
		self.sendButton = Button(self.window, image=self.i_sendButton, command=self.send, state=DISABLED)
		self.sendButton.grid(row=2, column=4, pady=20)
		self.root.mainloop()

	def reset(self):
		if (self.modep == 1): print("Reset")
		self.arrows = 1
		self.c_joystick = 0
		self.user_type = 0
		self.it = 0
		self.sec = 0
		self.i_changeId = PhotoImage(file=self.path + "/Img/id.png")
		self.userId.configure(image=self.i_changeId)
		self.userId.image = self.i_changeId
		self.i_changeDes = PhotoImage(file=self.path + "/Img/des0.png")
		self.userDes.configure(image=self.i_changeDes)
		self.userDes.image = self.i_changeDes
		self.upButton.config(state=NORMAL)
		self.downButton.config(state=NORMAL)
		self.time.config(fg="green", text="00", state=DISABLED)
		self.resetButton.config(state=DISABLED)
		self.speakButton.config(state=DISABLED)
		self.stopButton.config(state=DISABLED)
		self.playButton.config(state=DISABLED)
		self.sendButton.config(state=DISABLED)
		try:
			os.remove('audio.wav')
		except:
			if (self.modep == 1): print("No file .wav to delete")
		try:
			os.remove('c_audio.mp3')
		except:
			if (self.modep == 1): print("No file .mp3 to delete")
		
	def up(self):
		if self.arrows == 1:
			if (self.modep == 1): print("Up")
			if self.c_joystick == 0:
				self.c_joystick = 0
			else:
				if self.c_joystick != 1:
					self.c_joystick = self.c_joystick - 1
				else:
					self.c_joystick = 1
			self.change_photo(self.c_joystick)

	def down(self):
		if self.arrows == 1:
			if (self.modep == 1): print("Down")
			if self.c_joystick != 5:
				self.c_joystick = self.c_joystick + 1
			else:
				self.c_joystick = 5
			self.change_photo(self.c_joystick)

	def chosenID(self, event):
		if self.arrows == 1:
			if self.c_joystick != 0 and self.user_type == 0:
				if (self.modep == 1): print("Click ID label")
				self.user_type = 1     # Change user type to destination
				self.c_joystick = 0
				self.resetButton.config(state=NORMAL)
				self.i_changeDes = PhotoImage(file=self.path + "/Img/des.png")
				self.userDes.configure(image=self.i_changeDes)
				self.userDes.image = self.i_changeDes

	def chosenDes(self, event):
		if self.arrows == 1:
			if self.c_joystick != 0 and self.user_type == 1:
				if (self.modep == 1): print("Click Destination label")
				self.arrows = 0
				self.upButton.config(state=DISABLED)
				self.downButton.config(state=DISABLED)
				self.speakButton.config(state=NORMAL)

	def change_photo(self, c_joystick):
		self.c_joystick = c_joystick
		self.image_map = {
        1: "user1.png",
        2: "user2.png",
        3: "user3.png",
        4: "user4.png",
        5: "user5.png"
    	}
		self.image_filename = self.image_map.get(self.c_joystick)
		if self.image_filename:
			if self.user_type == 0:
				self.i_changeId = PhotoImage(file=self.path + "/Img/" + self.image_filename)
				self.userId.configure(image=self.i_changeId)
				self.userId.image = self.i_changeId
			else:
				self.i_changeDes = PhotoImage(file=self.path + "/Img/" + self.image_filename)
				self.userDes.configure(image=self.i_changeDes)
				self.userDes.image = self.i_changeDes

	def record(self):
		if (self.modep == 1): print("Record")
		self.it = 0
		self.rec = Recorder(self.modep)     # Construct recorder object
		self.start_time = time.time()
		self.time.config(state=NORMAL)
		self.speakButton.config(state=DISABLED)
		self.stopButton.config(state=NORMAL)
		self.rec.start()
		self.time_flag = True
		self.timing = threading.Thread(target=self.timer)
		self.timing.start()

	def stop(self):
		if (self.modep == 1): print("Stop recording")
		self.time_flag = False
		self.seconds = (round(time.time() - self.start_time))
		self.stopButton.config(state=DISABLED)
		self.playButton.config(state=NORMAL)
		self.sendButton.config(state=NORMAL)
		if self.it == 0:
			if (self.modep == 1): print ("Recorder time: ", self.seconds)
			self.it = 1
			self.rec.setStop()

	def play(self):
		if (self.modep == 1): print("Playing audio")
		self.rec.play_audio()
				
	def send(self):
		if (self.modep == 1): print("Sending message")
		self.speakButton.config(state=DISABLED)
		self.stopButton.config(state=DISABLED)
		self.playButton.config(state=DISABLED)
		self.sendButton.config(state=DISABLED)
		self.rec.convert_file()

	def timer(self):
		if self.time_flag == True:
			self.sec += 1
			self.secs = self.sec
			if self.secs < 10:
				self.secs = "0" + str(self.secs)
			if self.sec <= 50:
				self.time['text'] = str(self.secs)
			if self.sec < 51:
				self.process = self.time.after(1000, self.timer)
			if self.sec == 40:
				self.time.config(fg="yellow")
			if self.sec == 50:
				self.time.config(fg="red")
			if self.sec > 50:
				self.stop()
			
scr = Screen(1)