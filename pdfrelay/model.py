#!/usr/bin/env python

class ConversionJob(object):
	"""Container class for passing around job data"""
	def __init__(self, options):
		self.html = options['html']
		self.arguments = []
		self.metadata = {}
		self.pdf = None

		if 'arguments' in options.keys():
			self.arguments = options['arguments']

		for k,v in options.items():
			if k.startswith('metadata'):
				self.metadata[k[8:]] = v
			elif k not in ('html', 'arguments'):
				self.arguments.append(k)
				self.arguments.append(v)
