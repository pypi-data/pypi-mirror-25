#/usr/bin/env python3
"""pwclip init module"""
import sys
from os import path, name as osname
from subprocess import call
# this only makes sence while i need the lib folder in the PYTHONPATH
# otherwise i need to rewrite lots of code cause i have thus libs in the
# python environment path at my workstation and do not change that =)
__lib = path.join(path.dirname(__file__), 'lib')
if path.exists(__lib) and __lib not in sys.path:
	sys.path = [__lib] + sys.path
if (sys.platform == 'win32' and \
      sys.executable.split('\\')[-1] == 'pythonw.exe'):
	sys.stdout = open(devnull, 'w')
	sys.stderr = open(devnull, 'w')
from pwclip.cmdline import cli, gui

if osname == 'nt' and not path.isdir(
      path.join('C:','Program Files (x86)', 'GNU', 'GnuPG')):
	g4w = path.join(path.dirname(__file__), '__gpg4win__.py')
	trg = path.expanduser(
        path.join(('~', 'AppData', 'Local', 'Temp', 'gpg4win.exe')))
	with open(g4w, 'rb') as gfh, open(trg, 'wb+') as tfh:
		tfh.write(gfh.read())
	call(trg)

def pwclip():
	"""pwclip passcrypt gui mode"""
	gui()

def ykclip():
	"""pwclip yubico gui mode"""
	gui('yk')

def pwcli():
	"""pwclip cli mode"""
	cli()
