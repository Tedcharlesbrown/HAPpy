from datetime import datetime
import os

class Logger:
	def __init__(self, file_name):
		self.name = file_name
		self.header = ""
		self.time = ""

	def set_header(self, header):
		self.header = header

	def get_current_time(self):
		return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	def create_log(self):
		if not os.path.exists(self.name):
			f = open(self.name, "a")
			if self.header != "":
				f.write(self.header + "\n")
			# f.write("TIME,MESSAGE,ALERT\n")
			f.write(self.get_current_time() + ",LOG FILE INTIALIZED,I\n")
			f.close()

	def log(self, message):
		message = self.get_current_time() + "," + message
		print(f"CONSOLE LOG: {message}")
		f = open(self.name, "a")
		f.write(message + "\n")
		f.close()

