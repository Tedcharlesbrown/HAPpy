'''
Copyright (C) 2023  Ted Charles Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
'''

import os
import subprocess
import json
import re
import ffmpeg  # ffmpeg-python

from autopytoexe_path import resource_path

import sys


class FFMPEG:
	def __init__(self):
		exstension = ".exe" if sys.platform == "win32" else ""
		ffmpeg_folder = resource_path('', False)
		self.ffmpeg_bin = resource_path("ffmpeg" + exstension, False)
		self.ffprobe_bin = resource_path("ffprobe" + exstension, False)
		self.ffplay_bin = resource_path("ffplay" + exstension, False)

		self.ffmpeg_version = None
		self.ffprobe_version = None
		self.ffplay_version = None

		# Check if the specified ffmpeg.exe file exists
		if os.path.exists(ffmpeg_folder):
			# ---------------------------------- FFMPEG ---------------------------------- #
			try:
				self.ffmpeg_version = subprocess.run([self.ffmpeg_bin, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.ffmpeg_version = self.ffmpeg_version.stdout.decode('utf-8').splitlines()[0]
				# print(self.ffmpeg_version)
			except subprocess.CalledProcessError as e:
				print("ERROR")
			# ---------------------------------- FFPROBE --------------------------------- #
			try:
				self.ffprobe_version = subprocess.run([self.ffprobe_bin, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.ffprobe_version = self.ffprobe_version.stdout.decode('utf-8').splitlines()[0]
				# print(self.ffprobe_version)
			except subprocess.CalledProcessError as e:
				print("ERROR")
			# ---------------------------------- FFPLAY --------------------------------- #
			try:
				self.ffplay_version = subprocess.run([self.ffplay_bin, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				self.ffplay_version = self.ffplay_version.stdout.decode('utf-8').splitlines()[0]
				# print(self.ffprobe_version)
			except subprocess.CalledProcessError as e:
				print("ERROR")

		ffmpeg._run.DEFAULT_FFMPEG_PATH = self.ffmpeg_bin
		ffmpeg._run.DEFAULT_FFPROBE_PATH = self.ffprobe_bin     
		ffmpeg._run.DEFAULT_FFPLAY_PATH = self.ffplay_bin     
	
	def __str__(self):
		return f"FFmpeg version: {self.ffmpeg_version}\nFFprobe version: {self.ffprobe_version}"
	
	def get_version(self, exe="ffmpeg"):
		if exe == "ffmpeg":
			return self.ffmpeg_version
		elif exe == "ffprobe":
			return self.ffprobe_version
		elif exe == "ffplay":
			return self.ffplay_version
		else:
			raise ValueError("Invalid argument.")

	@staticmethod
	def get_video_dimensions(self, input_path):
		cmd = [self.ffprobe_bin, '-v', 'error', '-select_streams', 'v:0',
			'-show_entries', 'stream=width,height', '-of', 'csv=p=0', input_path]
		output = subprocess.check_output(cmd).decode('utf-8').strip()
		width, height = map(int, output.split(','))
		return width, height


	@staticmethod
	def round_up_to_nearest_four(n):
		return (n + 3) & ~3  # Rounds up to the nearest multiple of 4

	def encode_to_hap(self, input_path, output_path, codec="hap_alpha", mode="scale", callback=None):
		width, height = self.get_video_dimensions(self, input_path)
		invalid_width = False
		invalid_height = False

		#CHECK IF WIDTH AND HEIGHT ARE DIVISIBLE BY 4
		if width%4 != 0:
			invalid_width = True
			width = self.round_up_to_nearest_four(width) 

		if height%4 != 0:
			invalid_height = True
			height = self.round_up_to_nearest_four(height)

		#TODO MOVE THIS TO APP
		if not os.path.exists(os.path.dirname(output_path)):
			os.makedirs(os.path.dirname(output_path))

		# Create the ffmpeg command
		cmd = [self.ffmpeg_bin,'-i', input_path]

		if mode == "pad":
			cmd.extend(['-vf', f'pad={width}:{height}:0:0:black'])
		elif mode == "stretch":
			cmd.extend(['-vf', f'scale={width}:{height}'])
		# elif mode == "scale":
		#     if invalid_width and invalid_height:
		#         print("Invalid width and height")
		#         cmd.extend(['-vf', f'scale={width}:{height}'])
		#     elif invalid_width:
		#         print("Invalid width")
		#         cmd.extend(['-vf', f'scale={width}:-1'])
		#     elif invalid_height:
		#         print("Invalid height")
		#         cmd.extend(['-vf', f'scale=-1:{height}'])
		#     else:
		#         print("Valid width and height")
		#         cmd.extend(['-vf', f'scale=-1:-1'])
		else:
			raise ValueError("Invalid mode.")
		

		cmd.extend([
			'-c:v', 'hap',
			'-format', codec, # hap, hap_alpha, hap_q
			'-y',
			# os.path.splitext(output_path)[0] + "_HAP.mov"
			output_path + ".mov"
		])

		print(" ".join(cmd))
		process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)


		# ----------------------------- PROGRESS CALLBACK ---------------------------- #

		duration_pattern = re.compile(r"Duration: (\d+:\d+:\d+\.\d+)")
		progress_pattern = re.compile(r"time=(\d+:\d+:\d+\.\d+)")

		duration = None
		for line in iter(process.stderr.readline, ""):
			if duration is None:
				match = duration_pattern.search(line)
				if match:
					duration = sum(float(x) * 60 ** i for i, x in enumerate(reversed(match.group(1).split(":"))))
			match = progress_pattern.search(line)
			if match:
				progress_time = sum(float(x) * 60 ** i for i, x in enumerate(reversed(match.group(1).split(":"))))
				progress_percentage = (progress_time / duration) * 100 if duration else 0
				if callback:
					callback(progress_percentage)

		# return_code = process.wait()
		# After FFmpeg finishes, make sure you set the progress to 100%.
		if callback:
			callback(100.0)
			return cmd, True


	def play(self, input_path):

		# additional_args = ['-vf', 'scale=800:-1', '-fast', '-infbuf', '-framedrop', "drawtext=text='Your Text Here':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2"]

		additional_args = [
			'-loop', '0',
			# '-window_title', f'{os.path.basename(input_path)}',
			'-vf',
			"scale=800:-1",
			'-fast',
			'-infbuf',
			'-framedrop'
		]

		cmd = [self.ffplay_bin] + additional_args + [input_path]

		process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)

		return process
	
	def probe(self, input_path):
		cmd = [
			self.ffprobe_bin,
			'-v', 'error',
			'-show_entries', 'format=duration,bit_rate',
			'-show_streams',
			'-of', 'json',
			input_path
		]
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		if result.returncode != 0:  # if ffprobe encountered an error
			raise RuntimeError(result.stderr)
		return json.loads(result.stdout)