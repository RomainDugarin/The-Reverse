import logging

class ReverseLogger(logging.Logger):

	__slots__ = [
        'name',
        'instance',
        'logfile',
		'logformat',
		'formatter'
		'handler'
        'env'
    ]
	
	def __init__(self, name, path="./", logformat=""):
		self.name = name
		self.instance = logging.getLogger(name)
		self.logfile = "{}{}.log".format(path,name)
		self.logformat = logformat or ("[%(asctime)s] %(levelname)-8s :: %(message)s")
		self.formatter = logging.Formatter(self.logformat)
		self.handler = logging.FileHandler(self.logfile, encoding="utf-8")

		self.handler.setFormatter(self.formatter)
		self.instance.addHandler(self.handler)
		self.instance.setLevel(logging.DEBUG)
		self.getInstance().info("Creation of the logging instance - {}/{}".format(self.name, self.logfile))

	def getInstance(self) -> logging.Logger : 
		return self.instance