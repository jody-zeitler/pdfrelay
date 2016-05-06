class PdfRelayException(Exception):

	def __init__(self, *args, **kwargs):
		super(PdfRelayException, self).__init__(args, kwargs)

class JobError(PdfRelayException):
	"""Issue with the parameters of the conversion job"""

class EngineError(PdfRelayException):
	"""Engine process spawning/execution error"""

class MetadataError(PdfRelayException):
	"""An error occurred in the retrieval or saving of PDF metadata"""
