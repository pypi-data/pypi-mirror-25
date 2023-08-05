import wissen
from wissen import binfile
from wissen.lib import logger as loggerlib
import os, codecs, glob, json

resource_dir = None

def add_document (indexer, doc):
	document = wissen.document ()	
	document.content (doc ['document'])
	if 'snippet' in doc:
		document.snippet (doc ['snippet'])
	for name, opt in doc ['fields'].items ():
		if name == "_id":			
			data = str (opt)
			lang = 'un'
			ftype = wissen.STRING
		else:	
			data = opt.get ('data')
			lang = opt.get ('lang', 'un')
			ftype = opt.get ('type')
			if not ftype:
				raise TypeError ('Type of field is required')
		document.field (name, data, ftype, lang)
	indexer.add_document (document)

def getdir (*d):
	global resource_dir	
	return os.path.join (resource_dir, *d)

def delete (col, opt, deletables):
	global log
	
	opt ['searcher']['remove_segment'] = 0
	searcher = col.get_searcher (**opt ['searcher'])
	if searcher.si.getN () == 0:
		searcher.close ()
		return []
	
	for qs in deletables:
		qs ["commit"] = False
		searcher.delete (**qs)
		
	searcher.commit ()	
	searcher.close ()	
	log ('delete %d documents' % len (deletables))	
	return []
		
def index (path):	
	global log
	
	alias = os.path.split (path) [-1]
	if alias [0] in "#-":
		return
		
	with codecs.open (path, "r", "utf8") as f:
		colopt = json.loads (f.read ())
	
	colopt ['data_dir'] = [getdir (os.path.normpath(d)) for d in colopt ['data_dir']]
	queue_dir = colopt ['data_dir']
	if type (queue_dir) is list:
		queue_dir = queue_dir [0]
	
	queue_dir = os.path.join (queue_dir, ".que")
	queues = [(q, os.path.getmtime (q)) for q in glob.glob (os.path.join (queue_dir, 'que.*')) if not q.endswith (".lock")]
	if not queues:
		log ("nothing to for %s in %s" % (os.path.split (path) [-1], os.path.dirname (path)))
		return
		
	queues.sort (key = lambda x: x [-1])
	deletables = []
	
	analyzer = wissen.standard_analyzer (3000, 1, **colopt ['analyzer'])
	col = wissen.collection (
	  indexdir = colopt ['data_dir'],
	  mode = wissen.APPEND,
	  analyzer = analyzer
	)

	deleted = 0
	for qfile, mtime in queues:		
		bf = binfile.BinFile (qfile, "r")
		while 1:
			try: cmd = bf.readVInt ()
			except OSError:
				bf.close ()
				break
			
			try:
				doc = json.loads (bf.readZBytes ().decode ("utf8"))
			except (OSError, MemoryError):
				bf.close ()
				break
			
			if cmd == 1:
				qs = doc.get ("query")				
				deleted += 1
				deletables.append (qs)				
				if len (deletables)	== 1000:
					deletables = delete (col, colopt, deletables)
	
	if deletables:
		deletables = delete (col, colopt, deletables)	
	log ('delete %d documents in this session' % len (deletables))	
			
	indexer = col.get_indexer (**colopt ['indexer'])
	for qfile, mtime in queues:		
		bf = binfile.BinFile (qfile, "r")
		while 1:
			try: cmd = bf.readVInt ()				
			except OSError:
				bf.close ()
				break
				
			if cmd == 1:	 # just delete
				continue
			
			try:
				doc = json.loads (bf.readZBytes ().decode ("utf8"))
			except (OSError, MemoryError):
				bf.close ()
				break
				
			add_document (indexer, doc)
		
		log ('delete que %s' % qfile)	
		os.remove (qfile)
		
	indexer.close (optimize = deleted)
		
			
if __name__ == "__main__":
	import sys, getopt
	
	log = loggerlib.screen_logger ()
	argopt = getopt.getopt(sys.argv[1:], "l:", ["log="])

	for k, v in argopt [0]:
		if k == "-l" or k == "--log":
			log = loggerlib.multi_logger ([log, loggerlib.rotate_logger (v, "wissen", "daily")])
			
	wissen.configure (1, log)
	try:
		resource_dir = argopt [1][0]
	except IndexError:
		print ('Usage: mirror.py resource_dir')	
		print ('  ex. mirror.py /var/tmp/wissen')	
		sys.exit ()
		
	conf_dir = os.path.join (resource_dir, "models", ".config")
	for alias in os.listdir (conf_dir):
		log ("starting index for %s" % alias)
		try:
			index (os.path.join (conf_dir, alias))
		except:
			log.trace ()			
		log ("index done for %s" % alias)
		