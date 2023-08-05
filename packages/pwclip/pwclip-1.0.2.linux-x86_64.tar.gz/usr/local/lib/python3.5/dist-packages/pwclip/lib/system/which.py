"""which module to find executables"""
from os import X_OK, access, environ, path

def which(prog):
	"""which function like the linux 'which' program"""
	for path in environ['PATH'].split(':'):
		if access(path.join(path, prog), X_OK):
			return path.join(path, prog)
