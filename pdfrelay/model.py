#!/usr/bin/env python

class ConversionJob(object):
	"""Container class for passing around job data"""
	
	def __init__(self, options):
		self.html = options.pop('html')
		self.arguments = options.pop('arguments', [])
		self.metadata = options.pop('metadata', {})
		self.pdf = None
		self.error = None

		for k,v in options.items():
			if k.startswith('metadata'):
				self.metadata[k[8:]] = v
			else:
				self.arguments.append(k)
				self.arguments.append(v)
