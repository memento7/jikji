"""
	tests.utils
	---------------
	Test listener of application

	:author: Prev(prevdev@gmail.com)
"""

from jikji import utils


def test_getprop() :
	class TestClass :
		def __init__(self) :
			self.a = 3

	assert utils.getprop({'a': 1}, 'a') == 1
	assert utils.getprop({'a': 1}, 'b') == None
	assert utils.getprop(TestClass(), 'a') == 3
	assert utils.getprop(TestClass(), 'b') == None
	

def test_parse_varstr() :
	""" Test utils.parse_varstr
	"""
	assert utils.parse_varstr('/posts/{ board_id }/{post_id}', data={
		'board_id': 'free',
		'post_id': 33,
	}) == '/posts/free/33'


	assert utils.parse_varstr('/{ myvar1 }?json=\{"a": 1}', data={
		'myvar1': 4
	}) == '/4?json={"a": 1}'


	class TestClass :
		def __init__(self) :
			self.a = 1

	assert utils.parse_varstr('/{ a }/', data=TestClass()) == '/1/'