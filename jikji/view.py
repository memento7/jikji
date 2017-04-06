# -*- coding: utf-8 -*-
"""
	jikji/view
	---------------
	View, Page Class


	Jikji has a concept 'View', which is similar to 'Controller' on common backend framework
	One View has one 'URL rule', one 'View Function', and multiple 'Pages'.

	Usually, the controller has the role of taking the data from the model
	with the PARAMETERS in URL and returning the HTML with the View.

	In static web, PARAMETERS are provided in advance.
	There are many tuple set of parameters in ONE VIEW.

	Jikji calls the tuple 'Page'

	
	For example, 'Article View' has url rule '/posts/$1/$2'
	The sample pages for 'Article View' will have the following.

	/posts/dev/best-sublime-text-3-themes-of-2016
	/posts/dev/the-best-news-from-angulars-ng-conf

	:author: Prev(prevdev@gmail.com)
"""

import inspect
import os
from datetime import datetime
#from .app import Jikji
from . import utils


_processing_page_stack = []


def view(param=None, url_rule=None) :
	""" Decorate view(param is function) or find view(param is str)
	"""
	from .app import Jikji
	app = Jikji.getinstance()


	if url_rule :
		def decorator(func) :
			app.register_view(func, url_rule)
			
			def wrapper(*args, **kwargs):
				return func(*args, **kwargs)

			return wrapper

		return decorator


	if callable(param) :
		func = param
		app.register_view(func)

		def wrapper(*args, **kwargs):
			return func(*args, **kwargs)

		return wrapper

	elif type(param) == str :
		# Get View by id
		return app.views[param]


def virtualview(func) :
	""" Decorate virtualview
	"""
	from .app import Jikji
	app = Jikji.getinstance()


	app.register_virtualview(func)

	return func


def nowpage() :
	""" Get meta info of now-processing template
	"""
	global _processing_page_stack
	if len(_processing_page_stack) == 0:
		return None
	return _processing_page_stack[-1]



def render_template(template_path, **context) :
	""" Render template and return result
	"""
	from .app import Jikji
	app = Jikji.getinstance()
	

	if os.path.splitext(template_path)[1] == '' :
		template_path += '.html'

	context['_page'] = {
 		'url': nowpage().geturl(),
 		'template': template_path,
 		'render_time': datetime.now(),
 		'params': nowpage().params,
	}

	tpl = app.jinja_env.get_template(template_path)
	return tpl.render( context )



class View() :

	@staticmethod
	def parse_id(view_func, basepath) :
		""" Parse id from view_func and basepath
		"""

		# Get module of function
		module = inspect.getmodule(view_func)
		
		# Get relation path by module and basepath
		modulepath = os.path.relpath(module.__file__, basepath)
		rv = []
		for p in os.path.split(modulepath) :
			p2 = os.path.splitext(p)[0]
			if p2 :
				rv.append( p2 )

		rv.append(view_func.__name__)
		return '.'.join(rv)




	def __init__(self, id, view_func, url_rule=None, options=None) :
		""" View Constructor
		:param id: ID of view
		:param view_func: Function matched to view.
						  Page's content is generated by view_func call.
		:param url_rule: Rule of URL. One view has one URL RULE.
						 ex) /posts/$1/$2
						 Pages in views are classified by params in url rule
		:param options: Option param
		"""
		
		self.id = id
		self.view_func = view_func
		self.url_rule = url_rule
		self.options = options
		self.pages = []



	def addpage(self, *params) :
		""" Add page to View
		:param *params: Data Param in View's URL Rule ($1, $2, $3)
		"""
		self.pages.append(Page(self, params))



class Page :
	def __init__(self, view, params) :
		""" Page Constructor
		:param view: Target View
					 View and Page are mapped in 1:n relationship
		:param params: Params of Page inserted in url rule
		"""
		self.view = view
		self.params = params


	def getcontent(self) :
		""" Get content of page
		"""
		global _processing_page_stack

		_processing_page_stack.append(self)
		rv = self.view.view_func(*self.params)
		_processing_page_stack.pop()

		return rv


	def geturl(self) :
		""" Get url of page by matching URL rule and params
		"""
		url = self.view.url_rule

		for index, param in enumerate(self.params) :
			url = url.replace('$%d' % (index+1), str(param))

		return url



class VirtualView(View) :
	def __init__(self, id, virtualview_func, options=None) :
		View.__init__(self, id, None, None, options)

		self.vview_func = virtualview_func

	
	def adddata(self, data) :
		for item in self.vview_func(data) :
			v = view(item[0])
			params = item[1:]

			self.pages.append( Page(v, params) )

