import sys
import os
import shlex
import html
from flask import Flask, request, render_template, make_response

from .engine import PdfEngine, MetadataEngine
from .model import ConversionJob


app = Flask(__name__)
app.debug = True

conversion_engine = None
metadata_engine = None


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')

	elif request.method == 'POST':
		if request.json:
			job = ConversionJob(request.json)
			return render_pdf(job)
		else:
			return 'Request must be made with JSON.'


@app.route('/form', methods=['POST'])
def form():
	options = {}
	options['arguments'] = shlex.split(request.form['commandLine'])
	options['--header-html'] = request.form['headerInput']
	options['html'] = request.form['htmlInput']
	options['--footer-html'] = request.form['footerInput']
	options['metadataAuthor'] = request.form['metadataAuthor']
	options['metadataSubject'] = request.form['metadataSubject']
	job = ConversionJob(options)
	return render_pdf(job)


def render_pdf(job):
	bytes = conversion_engine.render(job)
	job.cleanup_files() # remove temp header and footer

	if len(bytes) < 64:
		return html.escape(job.error).replace('\n', '<br>')
	
	bytes = metadata_engine.add_metadata(bytes, job.metadata)

	resp = make_response(bytes)
	resp.headers['Content-Type'] = 'application/pdf'
	
	return resp


def initialize(engine_path):
	global conversion_engine
	global metadata_engine
	conversion_engine = PdfEngine( os.path.abspath(engine_path) )
	metadata_engine = MetadataEngine()
	print('Using conversion engine {}'.format(conversion_engine.binary_path))
	return app
