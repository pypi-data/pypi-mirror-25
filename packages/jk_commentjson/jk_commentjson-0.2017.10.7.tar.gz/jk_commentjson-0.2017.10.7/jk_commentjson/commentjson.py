try:
	import json
except ImportError:
	# If python version is 2.5 or less, use simplejson
	import simplejson as json

import re
import traceback
import codecs


class JSONLibraryException(Exception):
	''' Exception raised when the JSON library in use raises an exception i.e.
	the exception is not caused by `commentjson` and only caused by the JSON
	library `commentjson` is using.

	.. note::

		As of now, ``commentjson`` supports only standard library's ``json``
		module. It might start supporting other widely-used contributed JSON
		libraries in the future.
	'''

	def __init__(self, json_error=""):
		tb = traceback.format_exc()
		tb = '\n'.join(' ' * 4 + line_ for line_ in tb.split('\n'))
		message = [
			'JSON Library Exception\n',
			('Exception thrown by JSON library (json): '
			 '\033[4;37m%s\033[0m\n' % json_error),
			'%s' % tb,
		]
		Exception.__init__(self, '\n'.join(message))


def loads(text, **kwargs):
	''' Deserialize `text` (a `str` or `unicode` instance containing a JSON
	document with Python or JavaScript like comments) to a Python object.

	:param text: serialized JSON string with or without comments.
	:param kwargs: all the arguments that `json.loads <http://docs.python.org/
				   2/library/json.html#json.loads>`_ accepts.
	:raises: commentjson.JSONLibraryException
	:returns: dict or list.
	'''
	regex = r'\s*(#|\/{2}).*$'
	regex_inline1 = r'(:?(?:\s)*([A-Za-z\d\.{}]*)|((?<=\").*\"),?)(?:\s)*(((#).*)|)$'
	regex_inline2 = r'(:?(?:\s)*([A-Za-z\d\.{}]*)|((?<=\').*\'),?)(?:\s)*(((#).*)|)$'
	lines = text.split('\n')

	for index, line in enumerate(lines):
		if re.search(regex, line):
			if re.search(r'^' + regex, line, re.IGNORECASE):
				lines[index] = ""
			elif re.search(regex_inline2, line):
				lines[index] = re.sub(regex_inline2, r'\1', line)
			elif re.search(regex_inline1, line):
				lines[index] = re.sub(regex_inline1, r'\1', line)

	try:
		lineNo = 1
		for line in lines:
			#print(str(lineNo) + "\t" + line)
			lineNo += 1
		return json.loads('\n'.join(lines), **kwargs)
	except Exception as e:
		raise JSONLibraryException(str(e))


def dumps(obj, **kwargs):
	''' Serialize `obj` to a JSON formatted `str`. Accepts the same arguments
	as `json` module in stdlib.

	:param obj: a JSON serializable Python object.
	:param kwargs: all the arguments that `json.dumps <http://docs.python.org/
				   2/library/json.html#json.dumps>`_ accepts.
	:raises: commentjson.JSONLibraryException
	:returns str: serialized string.
	'''

	try:
		return json.dumps(obj, **kwargs)
	except Exception as e:
		raise JSONLibraryException(str(e))


def _detectByBOM(path, defaultValue):
	with open(path, 'rb') as f:
		raw = f.read(4)		# will read less if the file is smaller
	for enc,boms in \
			('utf-8-sig',(codecs.BOM_UTF8,)),\
			('utf-16',(codecs.BOM_UTF16_LE,codecs.BOM_UTF16_BE)),\
			('utf-32',(codecs.BOM_UTF32_LE,codecs.BOM_UTF32_BE)):
		if any(raw.startswith(bom) for bom in boms):
			return enc
	return defaultValue



def loadFromFile(filePath, **kwargs):
	enc = _detectByBOM(filePath, kwargs.get("encoding", 'utf-8'))
	with codecs.open(filePath, 'r', enc) as f:
		try:
			if "encoding" in kwargs:
				del kwargs["encoding"]
			return loads(f.read(), **kwargs)
		except Exception as e:
			raise JSONLibraryException(str(e))



def load(fp, **kwargs):
	''' Deserialize `fp` (a `.read()`-supporting file-like object containing
	a JSON document with Python or JavaScript like comments) to a Python object.

	:param fp: a `.read()`-supporting file-like object containing a JSON
			   document with or without comments.
	:param kwargs: all the arguments that `json.load <http://docs.python.org/
				   2/library/json.html#json.load>`_ accepts.
	:raises: commentjson.JSONLibraryException
	:returns: dict or list.
	'''

	try:
		return loads(fp.read(), **kwargs)
	except Exception as e:
		raise JSONLibraryException(str(e))


def dump(obj, fp, **kwargs):
	''' Serialize `obj` as a JSON formatted stream to `fp` (a
	`.write()`-supporting file-like object). Accepts the same arguments as
	`json` module in stdlib.

	:param obj: a JSON serializable Python object.
	:param fp: a `.read()`-supporting file-like object containing a JSON
			   document with or without comments.
	:param kwargs: all the arguments that `json.dump <http://docs.python.org/
				   2/library/json.html#json.dump>`_ accepts.
	:raises: commentjson.JSONLibraryException
	'''

	try:
		json.dump(obj, fp, **kwargs)
	except Exception as e:
		raise JSONLibraryException(str(e))
