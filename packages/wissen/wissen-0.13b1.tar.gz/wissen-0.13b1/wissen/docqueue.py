from wissen import binfile
import os
import shutil
import random
import threading
import glob

class DocQueue:
	quename = "que"
	def __init__ (self, si):
		self.si = si
		self.que_dir = self.si.fs.getmaster ()
		self._tlock = threading.RLock ()
		self._plock = self.si.plock # process lock
		self.writer = None
		self.current = None		
		self.rollback_all ()
	
	def __detect_max_seq (self):	
		while 1:
			rn = random.randrange (100000, 999999)
			if not os.path.isfile (os.path.join (self.que_dir, "%s.%d.lock" % (self.quename, rn))) and not os.path.isfile (os.path.join (self.que_dir, "%s.%d" % (self.quename, rn))):
				return rn

	def rollback_all (self):
		for uncommit in glob.glob (os.path.join (self.que_dir, "%s.*.lock" % self.quename)):			
			os.remove (uncommit)
		
	def __call__ (self, method, doc):
		self.add (method, doc)
	
	def open (self):	
		self.current = self.__detect_max_seq ()
		self.writer = binfile.BinFile (os.path.join (self.que_dir, "%s.%d.lock" % (self.quename, self.current)), "w")
	
	def close (self, remove = 0):
		if not self.writer: return
		self.writer.close ()
		self.writer = None
		if remove:
			os.remove (os.path.join (self.que_dir, "%s.%d.lock" % (self.quename, self.current)))
		else:	
			shutil.move (
				os.path.join (self.que_dir, "%s.%d.lock" % (self.quename, self.current)),
				os.path.join (self.que_dir, "%s.%d" % (self.quename, self.current))
			)
			
	def rollback (self):
		with self._tlock:
			self.close (1)
			self.open ()
	
	def commit (self):
		with self._tlock:
			self.close ()
			self.open ()
		
	def add (self, method, doc):
		with self._tlock:
			if self.writer is None:			
				self.open ()
			self.writer.writeVInt (method)
			self.writer.writeZBytes (doc)
