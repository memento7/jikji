# -*- coding: utf-8 -*-
"""
	jikji/listener
	----------------
	Listening server for fast develop

	:author: Prev(prevdev@gmail.com)
"""

import os, shutil
import mimetypes
import flask
import jinja2

from .cprint import cprint
from .view import View

class Listener :

	def __init__(self, app) :
		""" Init Listener instance
		:param generator: Jikji Generator instance
		"""
		self.app = app
		self.generator = app.generator

	
		# merge pages to one variable in each views
		npages = {}
		for view in View.getviews() :
			for page in view.pages :
				url = self.format_url( page.geturl() )
				npages[url] = page

		self.pages = npages


	def listen(self, port, host) :
		""" Start listening HTTP server with Flask
		"""
		cprint.section('Listening %s pages' % len(self.pages))
		for url in self.pages :
			cprint.line('/' + url)

		cprint.section('Open Local Server with Flask (%d pages)' % len(self.pages))

		flaskapp = flask.Flask(__name__)
		flaskapp.add_url_rule('/', 'index', self.response)
		flaskapp.add_url_rule('/<path:url>', 'response', self.response)
		flaskapp.run(port=port, host=host)

		self.flaskapp = flaskapp



	def format_url(self, url) :
		""" Format url to check equals
		"""
		if len(url) >= 10 and url[-10:] == 'index.html' :
			url = url[:-10]

		if len(url) >= 1 and url[0] == '/' :
			url = url[1:]
		# if len(url) > 1 and url[-1] == '/' :
		# 	url = url[0:-1]

		return url


	def response(self, url='') :
		""" Response content from url
			If url exists in pages.xml data, render template in realtime and return output
			Else, Find files in assets dir.
		"""
		url = self.format_url(url)

		if url in self.pages :
			page = self.pages[url]

			# Reload view-model file
			page.view.init_viewmodel(self.app.settings)

			# Render template with jinja
			output = self.generator.generate_page(
				template_path = page.view.template_path,
				context = page.getcontext()
			)
			
			return output, 200



		# Check for static files
		asset_path = os.path.join(self.app.settings.STATIC_ROOT, url)
		
		if os.path.isfile(asset_path) :
			with open(asset_path, 'rb') as file :
				content = file.read()

			type = mimetypes.guess_type(url)[0]
			return content, 200, {'Content-type': type}


		filename = os.path.basename(url)

		if len(filename) > 0 and '.' not in filename :
			return flask.redirect(url + '/', code=302)

		return '<h1 align="center">404 NOT FOUND</h1>', 404
		

