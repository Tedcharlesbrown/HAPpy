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
		# return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		return datetime.now().strftime("%H:%M:%S")

	def create_log(self):
		"""If the log file doesn't exist, create it and write the header. (Returns True if the file already exists.))"""
		if not os.path.exists(self.name):
			f = open(self.name, "a")
			if self.header != "":
				f.write(self.header + "\n")
			f.write("LOG FILE INTIALIZED\n")
			f.close()
			return False
		else:
			return True


	def write_log(self, message):
		f = open(self.name, "a")
		f.write(message + "\n")
		f.close()

	def log(self, message, type=None):
		if type is None:
			type = "LOG"
		message = f"{self.get_current_time()},{type},{message}"
		print(f"CONSOLE LOG: {message}")
		self.write_log(message)

