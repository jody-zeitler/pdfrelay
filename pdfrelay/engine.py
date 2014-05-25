#!/usr/bin/env python3

import sys
import os
import subprocess
import re

class PdfEngine(object):
	"""Engine that controls process management of the PDF converter"""
	def __init__(self, binary_path, process_timeout=30):
		if not os.access(binary_path, os.X_OK):
			raise Exception('PDF engine binary path is not executable.')
		self.binary_path = binary_path
		self.process_timeout = process_timeout


	def render(self, html, arguments):
		arguments = list(arguments) # copy
		arguments.insert(0, self.binary_path)
		arguments.append('-')
		arguments.append('-')

		print('spawning process: {}'.format(' '.join(str(x) for x in arguments)))
		proc = subprocess.Popen(
			arguments,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
		out,errs = proc.communicate(html.encode(), self.process_timeout)
		
		if errs and len(errs) > 0:
			print(errs.decode())

		return out



class MetadataEngine(object):
	"""Engine that works with PDF bytes to manipulate metadata"""
	def __init__(self):
		self.defaults = {}

	def add_metadata(self, inbytes, metadata):
		"""Inject metadata in the proximity of already-known values"""
		m = re.search(rb'/Producer.*', inbytes)
		if not m:
			raise Exception('Producer metadata field is not found.')

		producer = m.group(0)
		newattributes = producer + b'\n/Author (Jody Zeitler)'

		outbytes = re.sub(rb'/Producer.*', newattributes, inbytes)

		return outbytes
