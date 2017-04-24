"""
	Jikji/cli
	----------------
	Command line application for jikji app.
	
	:author: Prev(prevdev@gmail.com)
	
"""

import sys
import click

from .app import Jikji
from .generator import Generator
from .listener import Listener


cli_help = """\
\b
Static website generator based on RESTFul Server *~*
You can read guide from https://github.com/Prev/jikji

\b 
Example Usage:
   $ jikji <mysite> generate
   $ jikji <mysite> cache list

"""



@click.group(help=cli_help)
@click.argument('sitepath', metavar='<sitepath>', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, sitepath) :
	ctx.obj['SITEPATH'] = sitepath
	ctx.obj['APP'] = Jikji( sitepath )



"""
Command for generate
Usage:
	jikji <sitepath> generate

"""
@cli.command('generate', short_help="Generate static site")
@click.option('--clear', '-h', is_flag=True, default=False)
@click.pass_context
def generate_command(ctx, clear) :
	""" Generate static site
	"""
	app = ctx.obj['APP']
	r = app.generate(clear=clear)
	
	sys.exit(r)


"""
Open listening server for develop
Usage:
	jikji <sitepath> listen

"""
@cli.command('listen')
@click.option('--host', '-h', default='0.0.0.0')
@click.option('--port', '-p', default=7000)
@click.pass_context
def listen_command(ctx, host, port) :
	""" Generate static site
	"""
	app = ctx.obj['APP']

	listener = Listener(app)
	listener.listen(host=host, port=port)



def main(as_module=False) :
	""" Main function called from shell or __main__.py
	
	:param as_module: True if called from __main__
	"""
	name = __package__

	if as_module :
		name = 'python -m ' + name

	cli(prog_name = name, obj={})

