from wissen.lib import unistr
import json

class Document:
	def __init__ (self, _id = None, content = None):
		self._id = _id
		self.fields = {}
		self.data = None
		self.stored = []
		self.summary = None		
		if content:
			self.set_content (content)
	
	def add_content (self, content, option = []):
		# any encoding even allowed python objects
		if self.data: 
			self.stored.append (self.data)
			self.data = None
		self.stored.append ((content, option))
			
	def field (self, name, value, ftype = "Text", lang = "en", encoding = None, option = {}):
		self.fields [name] = (unistr.makes (value, encoding), ftype, lang, option)
	
	def content (self, content):
		# any encoding even allowed python objects
		if self.stored: raise ValueError("Already got content(s)")
		self.data = content
	
	def snippet (self, text, option = {}, encoding = None):
		self.summary = (unistr.makes (text, encoding), option)
	
	def as_dict (self):
		fields = {}
		if self._id:
			fields ['_id'] = str (self._id)			
		for k, v in self.fields.items ():
			fields [k] = {'data': v [0], 'type': v [1], 'lang': v [2], 'options': v [3]}
		
		return {
			'sinppet': self.summary,
			'document': self.data,
			'fields': fields
		}
	
	def as_json (self):
		return json.dumps (self.as_dict ())
		
