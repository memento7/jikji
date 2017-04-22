"""
	Jikji
	----------------
	Static website generator adapting View-ViewModel Pattern 
	
	:author: Prev(prevdev@gmail.com)
	:license: MIT

"""

__version__ = '2.0.0'

from jikji.app import Jikji, addpage, addpagegroup, getview
from jikji.view import render_template, register_view