from ... import _delune
from ...util import util
from . import segmentwriter
from . import fieldwriter
import types

class WDocument:
	def __init__ (self, docId, si, fw, analyzer):
		self.docId = docId
		self.si = si
		self.fw = fw
		self.analyzer = analyzer
		self.stored = []
		self.summary = ""

	def addField (self, type, name, value, lang, option = []):
		num = self.si.setFieldInfo (name, type)
		self.fw (type, self.docId, num, name, value, lang, option)

	def transport (self, text, lang, option):
		if self.analyzer and "removehtml" in option:
			temp = text
			text = self.analyzer.htmlStrip (temp)

		elif self.analyzer and "formalize" in option:
			text = self.analyzer.formalize (text)

		if self.analyzer and "transform" in option:
			text = self.analyzer.transform (text)

		# WARNING: always last processing
		if self.analyzer and "stem" in option:
			text = self.analyzer.term (text, lang)
			if text is None:
				text = []

		return text
	
	def setData (self, obj):
		self.stored = obj
	
	def addSummary (self, summary, lang, option = []):
		self.summary = self.transport (summary, lang, option)


class IndexWriter:
	def __init__ (self, si, analyzer):
		self.si = si
		self.analyzer = analyzer
		self.tcache = {}

		self.fw = None
		self.segment = None
		self.newSegment ()

	def close (self):
		if self.segment:
			self.segment.close ()
		self.segment = None

	def newSegment (self):
		self.segment = segmentwriter.SegmentWriter (self.si)
		self.fw = fieldwriter.FieldWriter (self.segment, self.analyzer)

	def getNumDoc (self):
		return self.segment.numDoc

	def getMemUsage (self):
		return self.segment.getMemUsage ()

	def newWDocument (self):
		docId = self.segment.newdocid ()
		d = WDocument (docId, self.si, self.fw, self.analyzer)
		return d

	def addWDocument (self, d):
		storeds = [util.serialize (each) for each in d.stored]
		self.segment.writeField (storeds, d.summary)
		d = None

	#---------------------------------------------------------------------------
	# flushing
	#---------------------------------------------------------------------------
	def flush (self, final):
		if self.segment:
			self.segment.flush ()
			self.segment = None

		if not final:
			self.newSegment ()
