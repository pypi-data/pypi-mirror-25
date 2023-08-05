from delune.lib import unistr
import json

class Document:
	def __init__ (self, _id = None, analyzer = None):
		self._id = _id
		self.fields = {}
		self.stored = []
		self.summary = None
		self.analyzer = analyzer
	
	def field (self, name, value, ftype = "Text", lang = "en", encoding = None, option = []):
		if type (option) is str:
			option = option.split ()
		self.fields [name] = (unistr.makes (value, encoding), ftype, lang, option)
	
	def documents (self, contents):
		# set one shot, used by schduled indexer
		self.stored = contents
		
	def document (self, content):		
		# any encoding even allowed python objects
		self.stored.append (content)
		
	def snippet (self, text, lang = "en", option = [], encoding = None):
		if type (option) is str:
			option = option.split ()
		self.summary = (unistr.makes (text, encoding), lang, option)
	
	def as_dict (self):
		fields = {}
		if self._id:
			fields ['_id'] = str (self._id)			
		for k, v in self.fields.items ():
			fields [k] = {'data': v [0], 'type': v [1], 'lang': v [2], 'options': v [3]}
		
		return {
			'sinppet': self.summary,
			'documents': self.stored,
			'fields': fields
		}
	
	def as_json (self):
		return json.dumps (self.as_dict ())
		
