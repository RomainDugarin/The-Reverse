from discord import Colour

class DALRole():

	__slots__=[
		'name',
		'permission',
		'colour',
		'hoist',
		'mentionable',
		'reason',
		'regex',
		'position',
		'uniqueness',
		'magicmultiplier',
		'oid',
		'supplies'
	]
	
	def __init__(self,
		name='new role',
		permissions=None,
		colour=0xffffff,
		hoist=False,
		mentionable=False,
		reason="Create for the Drug Addict Lair Game of Kings.",
		regex="",
		position=0,
		uniqueness=0,
		magicmultiplier=1.2,
		oid=None,
		supplies=0):
		pass

	