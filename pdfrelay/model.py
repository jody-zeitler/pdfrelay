import os
import random

from .exception import *

class ConversionJob(object):
	"""Container class for passing around job data"""
	
	def __init__(self, options):
		self.html = options.pop('html', None)
		self.url = options.pop('url', None)
		if not (self.html or self.url):
			raise JobError("'html' or 'url' parameter not supplied")

		self.arguments = options.pop('arguments', [])
		self.metadata = options.pop('metadata', {})
		self.pdf = None
		self.error = None

		self.header_file = None
		self.footer_file = None

		for k,v in options.items():
			if k.startswith('metadata'):
				self.metadata[k[8:]] = v
			elif k == '--header-html':
				self.arguments.append(k)
				self.arguments.append( self.make_header(v) )
			elif k == '--footer-html':
				self.arguments.append(k)
				self.arguments.append( self.make_footer(v) )
			else:
				self.arguments.append(k)
				self.arguments.append(v)

	def make_header(self, html):
		self.header_file = '/dev/shm/pdfrelay_header_{}.html'.format(random.randint(1000000, 9999999))
		with open(self.header_file, 'w') as outfile:
			outfile.write(html)
		return self.header_file

	def make_footer(self, html):
		self.footer_file = '/dev/shm/pdfrelay_footer_{}.html'.format(random.randint(1000000, 9999999))
		with open(self.footer_file, 'w') as outfile:
			outfile.write(html)
		return self.footer_file

	def cleanup_files(self):
		if self.header_file and os.path.isfile(self.header_file):
			os.remove(self.header_file)
		if self.footer_file and os.path.isfile(self.footer_file):
			os.remove(self.footer_file)
