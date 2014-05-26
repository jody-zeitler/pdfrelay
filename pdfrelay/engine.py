#!/usr/bin/env python3

import sys
import os
import subprocess
import re

from .exception import *

class PdfEngine(object):
	"""Engine that controls process management of the PDF converter"""
	
	def __init__(self, binary_path, process_timeout=30):
		
		if not os.access(binary_path, os.X_OK):
			raise EngineError('PDF engine binary path is not executable.')
		
		self.binary_path = binary_path
		self.process_timeout = process_timeout


	def render(self, job):
		html = job.html

		arguments = list(job.arguments) # copy
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
			job.error = errs.decode()

		return out



class MetadataEngine(object):
	"""Engine that works with PDF bytes to manipulate metadata"""
	
	def __init__(self):
		self.defaults = {}

	def add_metadata(self, inbytes, metadata):
		"""Inject metadata in the proximity of already-known values"""
		
		m = re.search(rb'/Producer.*', inbytes)
		if not m:
			raise MetadataError('Producer metadata field is not found.')

		# used as a proximity basis for injecting new metadata
		producer_field = m.group(0)
		new_attributes = producer_field
		outbytes = inbytes

		for k,v in metadata.items():
			bkey = b'/' + k.encode('ascii')
			bval = v.encode('utf-8')
			m = re.findall(bkey, outbytes)
			if len(m) == 1:
				outbytes = re.sub(bkey + b'.*', bkey + b' (' + bval + b')', outbytes)
			elif len(m) > 1:
				raise MetadataError('Field defined more than once.')
			else:
				new_attributes += b'\n' + bkey + b' (' + bval + b')'

		outbytes = re.sub(rb'/Producer.*', new_attributes, outbytes)

		return outbytes
