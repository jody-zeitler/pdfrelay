PDFRelay
========

PDFRelay is a Flask app that renders HTML into a PDF file over a REST API. It is a web wrapper for wkhtmltopdf with metadata injection as an added bonus.

It's designed to be a service for one or more web applications to deliver PDF renditions without messing with process management or additional plugins. Being that the input is not sanitized before being passed to the render process, do not expose this server to the general public.

Install
-------

Get Flask and uWSGI from the requirements.txt file:

	pip install -r requirements.txt

The wkhtmltopdf engine is not packaged with the repo - get it at http://wkhtmltopdf.org and put it in the `bin/` directory. The path to the executable is passed within `wsgi.py`.

Usage
-----

If uWSGI is set up properly, run the server with `start.sh`, or point your favorite WSGI server to `wsgi.py`. A GET request to `/` renders a test page with form controls. Enter some HTML and hit **Convert Markup** - it should send you a PDF.

A POST request to `/` takes in a JSON object holding command line arguments to wkhtmltopdf as key-value pairs. All options for the executable are passed directly to the binary. Place metadata fields in a `metadata` object. The main input can be supplied as markup in `html` or a remote URL in `url`.

```
{
	"html": "<html><body>Hello World!</body></html>",
	"--header-html": "This will appear at the top of <strong>every</strong> page",
	"--footer-html": "And this will be at the <em>bottom</em> of each page",
	"--margin-top": "10",
	"--margin-bottom": "10",
	"--javascript-delay": "2000",
	"metadata": {
		"Author": "Jody Zeitler",
		"Subject": "Example PDF"
	}
}
```

Notes
-----

Queuing is managed by the web server itself. If the server has 4 processes with 2 threads each, 8 concurrent render processes could be running at any point. This is sufficient as an independent web app. If it were included as part of a larger app with more threads, an internal process manager will need to throttle resources consumed by wkhtmltopdf.

There are a handful of PDF manipulation libraries in pip, some of which are able to add metadata. However those that I've tried had unintended side effects (loss of thumbnail, document restructuring). The metadata injection piece is my own creation, and is more or less manual byte manipulation. Once I find a decent (and up-to-date) library I will hand it off, because it's icky. That being said, it has full Unicode support!
