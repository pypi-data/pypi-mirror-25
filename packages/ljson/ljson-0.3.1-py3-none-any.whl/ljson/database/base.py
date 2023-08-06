#!/usr/bin/python3

"""
This module provides basic database functionality using
ljson.

A ljson database is basically a set of tables.
To provide the user with some comfort there 
are some special tables describing the database.

The database is represented in a directory on the disk.

"""

from ..base import disk

class Database(object):
	"""
	The database handle used by programs.

	``info`` is an ljson table containing some information about the
	database,
	``tables`` is a ljson table describing the data tables.
	"""
	def __init__(self, info, tables, read_tables = True, table_type = disk.Table):
		self.info = info
		self.tables = tables
		self.read_tables = read_tables
		self.table_type = table_type
		self.active_tables = {} # used to store loaded tables

	def on_table_requested(self, name, force_load = False):
		if(len(self.tables[{"name":name}]) == 0):
			raise IOError("failed to open table '{}': unknow".format(name))
		if(not force_load and name in self.active_tables):
			return True
		if(self.read_tables and not name in self.active_tables):
			self.active_tables[name] = table_type.from_file(open(self.tables[{"name":name}].getone("file"), "r+"))
			return
		if(self.read_tables and force_load):
			self.active_tables[name] = table_type.from_file(open(self.tables[{"name":name}].getone("file"), "r+"))
			return

	def on_table_created(self, name, filename, header):
		pass





