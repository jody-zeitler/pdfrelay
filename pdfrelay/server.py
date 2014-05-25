#!/usr/bin/env python3

import sys
import os
import shlex
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
	options['html'] = request.form['htmlInput']
	job = ConversionJob(options)
	return render_pdf(job)


def render_pdf(job):
	try:
		bytes = conversion_engine.render(job.html, job.arguments)
		bytes = metadata_engine.add_metadata(bytes, job.metadata)

		resp = make_response(bytes)
		resp.headers['Content-Type'] = 'application/pdf'
		resp.headers['Content-Disposition'] = "attachment; filename=test.pdf"
		
		return resp
	
	except Exception as e:
		return str(e)


def initialize(engine_path):
	global conversion_engine
	global metadata_engine
	conversion_engine = PdfEngine( os.path.abspath(engine_path) )
	metadata_engine = MetadataEngine()
	print('Using conversion engine {}'.format(conversion_engine.binary_path))
	return app
