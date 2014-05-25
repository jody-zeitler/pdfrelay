#!/usr/bin/env python3

import pdfrelay.server

app = pdfrelay.server.initialize('bin/wkhtmltopdf')

if __name__=='__main__':
	app.run()