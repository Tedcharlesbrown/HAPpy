'''
Copyright (C) 2023  Ted Charles Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
'''

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
		# message = f"{self.get_current_time()},{type},{message}"
		# print(f"CONSOLE LOG: {message}")
		# self.write_log(message)
		# Escape any double quotes in the message and then enclose the message in double quotes
		escaped_message = '"' + message.replace('"', '""') + '"'

		log_message = "{},{},{}".format(self.get_current_time(), type, escaped_message)
		print("CONSOLE LOG: {}".format(log_message))
		self.write_log(log_message)

