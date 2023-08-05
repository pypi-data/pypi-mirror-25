# 2017. 3. 13 by Hans Roh (hansroh@gmail.com)

from skitai.saddle import Saddle
import skitai
import wissen
from wissen.lib import pathtool
import os
import json
import codecs
import time
import shutil

app = Saddle (__name__)
app.config.numthreads = 1
app.last_maintern = time.time ()

def getdir (*d):
	return os.path.join (app.config.resource_dir, *d)

def is_json (request):
	return request.command == "post" and not request.get_header ('content-type', '').startswith ('application/x-www-form-urlencoded')

def normpath (path):
	if os.name == "nt":
		return path.replace ("/", "\\")
	return path.replace ("\\", "/")
			
def load_data (alias, numthreads, plock):
	with codecs.open (getdir ("models", ".config", alias), "r", "utf8") as f:
		colopt = json.loads (f.read ())			
		colopt ['data_dir'] = [getdir (normpath(d)) for d in colopt ['data_dir']]
		
	if 'classifier' in colopt:
		analyzer = wissen.standard_analyzer (10000, numthreads, **colopt ["analyzer"])
		col = wissen.model (colopt ["data_dir"], wissen.READ, analyzer, plock = plock)
		actor = col.get_classifier (**colopt.get ('classifier', {}))
	else:
		analyzer = wissen.standard_analyzer (8, numthreads, **colopt ["analyzer"])
		col = wissen.collection	(colopt ["data_dir"], wissen.READ, analyzer, plock = plock)	
		actor = col.get_searcher (**colopt.get ('searcher', {}))
		actor.create_queue ()
	wissen.assign (alias, actor)

def error (response, status, errcode, errmsg = "", errstack = None):
	return response (
		status, 
		json.dumps ({'errcode': errcode, "errmsg": errmsg, "errstack": errstack}), 
		[("Content-Type", "application: json")]
	)
		
#-----------------------------------------------------------------

@app.startup
def startup (wasc):
	app.config.numthreads = len (wasc.threads)
	wissen.configure (app.config.numthreads, wasc.logger.get ("app"), 16384, 128)
	pathtool.mkdir (getdir ("models", ".config"))
	for alias in os.listdir (getdir ("models", ".config")):
		if alias.startswith ("-"):
			with codecs.open (getdir ("models", ".config", alias), "r", "utf8") as f:
				colopt = json.loads (f.read ())
			for d in [getdir (normpath(d)) for d in colopt ['data_dir']]:
				if os.path.isdir (d):
					shutil.rmtree (d)
			os.remove (getdir ("models", ".config", alias))
		elif alias.startswith ("#"):
			continue
		else:
			load_data (alias, app.config.numthreads, wasc.plock)
  
@app.shutdown
def shutdown (wasc):
	wissen.shutdown ()

#-----------------------------------------------------------------

@app.before_request
def before_request (was):
	with app.lock:
		need_maintern = was.getlu ("wissen:collection") > app.last_maintern
		if need_maintern:
			app.last_maintern = time.time ()
	
	if need_maintern:
		for alias in os.listdir (getdir ("models", ".config")):			
			if alias [0] in "#-":
				if wissen.get (alias [1:]):
					wissen.close (alias [1:])
			elif not wissen.get (alias):						
				load_data (alias, app.config.numthreads, was.plock)					

	if was.request.args.get ('alias') and was.request.routed.__name__ != "config":
		alias = was.request.args.get ('alias')
		if not wissen.get (alias):
			return error (was.response, "404 Not Found", 40401, "resource %s not exist" % alias)
		
@app.failed_request
def failed_request (was, exc_info):
  return error (
  	was.response, 
  	"500 Internal Server Error", 
  	50000, 
  	errstack = app.debug and was.render_ei (exc_info, 2) or None
  )

#-----------------------------------------------------------------

@app.route ("/")
def index (was):
	return was.jstream ({'collections': list (wissen.status ().keys ())})

@app.route ("/<alias>", methods = ["GET", "POST", "PATCH", "DELETE", "OPTIONS"])
def config (was, alias, side_effect = ""):
	fn = getdir ("models", ".config", alias)
	if was.request.command == "get":
		if side_effect == "undo":
			for mark in "#-":
				if os.path.isfile (getdir ("models", ".config", mark + alias)):
					os.rename (
						getdir ("models", ".config", mark + alias),
						getdir ("models", ".config", alias)
					)
					was.setlu ("wissen:collection")
					return error (was.response, "201 Accept", 20100, "request accepted")
			return error (was.response, "404 Not Found", 20100, "resource already commited")
		
		if not wissen.get (alias):
			return error (was.response, "404 Not Found", 40401, "resource %s not exist" % alias)
			
		status = wissen.status (alias)
		conf = getdir ("models", ".config", alias)
		with codecs.open (conf, "r", "utf8") as f:
			colopt = json.loads (f.read ())		
			status ['colopt'] = {
				'data': colopt,
				'mtime': 	os.path.getmtime (conf),
				'size': 	os.path.getsize (conf),
				'path': conf
			}
		return was.jstream (status)
			
	if was.request.command == "delete":
		if not os.path.isfile (fn):
			return error (was.response, "404 Not Found", 40401, "resource not exist")
		
		a, b = os.path.split (fn)
		if side_effect == "data":
			newfn = os.path.join (a, "-" + b)
		else:
			newfn = os.path.join (a, "#" + b)		
		os.rename (fn, newfn)
		was.setlu ("wissen:collection")
		return was.jstream ({})
	
	for mark in "#-":
		if os.path.isfile (getdir ("models", ".config", mark + alias)):			
			return error (was.response, "406 Conflict", 40601, "removed resource is already exists, use UNDO")
			
	if was.request.command == "post" and wissen.get (alias):
		return error (was.response, "406 Conflict", 40601, "resource already exists")		
	elif was.request.command == "patch" and not wissen.get (alias):
		return error (was.response, "404 Not Found", 40401, "resource not exist")
			
	with codecs.open (fn, "w", "utf8") as f:
		f.write (was.request.body.decode ("utf8"))
	
	was.setlu ("wissen:collection")		
	return ''

#-----------------------------------------------------------------

@app.route ("/<alias>/locks", methods = ["GET", "OPTIONS"])
def locks (was, alias):
	return was.jstream ({"locks": wissen.get (alias).si.lock.locks ()})	

@app.route ("/<alias>/locks/<name>", methods = ["POST", "DELETE", "OPTIONS"])
def handle_lock (was, alias, name):	
	if was.request.command == "post":
		wissen.get (alias).si.lock.lock (name)		
		return ''
	wissen.get (alias).si.lock.unlock (name)
	return ''

#-----------------------------------------------------------------

@app.route ("/<alias>/commit", methods = ["GET", "OPTIONS"])
def commit (was, alias):
	wissen.get (alias).queue.commit ()
	return ''

@app.route ("/<alias>/rollback", methods = ["GET", "OPTIONS"])
def rollback (was, alias):
	wissen.get (alias).queue.rollback ()
	return ''

#-----------------------------------------------------------------

@app.route ("/<alias>/collection/<group>/<fn>", methods = ["GET", "OPTIONS"])
def getfile (was, alias, group, fn):
	s = wissen.status (alias)
	if group == "primary":
		path = os.path.join (s ["indexdirs"][0], fn)
	else:
		path = os.path.join (s ["indexdirs"][0], group, fn)
	return was.fstream (path)

@app.route ("/<alias>/segments/<group>/<fn>", methods = ["GET", "OPTIONS"])
def getsegfile (was, alias, group, fn):
	s = wissen.status (alias)
	seg = fn.split (".") [0]
	if group == "primary":
		if seg not in s ["segmentsizes"]:
			return error (was.response, "404 Not Found", 40401, "resource not exist")
		path = os.path.join (s ["segmentsizes"][seg][0], fn)	
	else:
		path = os.path.join (s ["indexdirs"][0], group, fn)
	return was.fstream (path)

#-----------------------------------------------------------------

@app.route ("/<alias>/documents", methods = ["POST", "OPTIONS"])
def add (was, alias, **args):		
	wissen.get (alias).queue (0, was.request.body)
	return ''

@app.route ("/<alias>/documents/<_id>", methods = ["GET", "PUT", "DELETE", "PATCH", "OPTIONS"])
def get (was, alias, _id, **args):
	if was.request.command == "get":
		return query (was, alias, q = "_id:" + _id, o = 0, f = 1)
	
	wissen.get (alias).queue (1, json.dumps ({"query": {'qs': "_id:" + _id}}))
	if was.request.command != "delete":
		wissen.get (alias).queue (0, was.request.body)
	return ''

#-----------------------------------------------------------------
	
@app.route ("/<alias>/search", methods = ["GET", "POST", "DELETE" "OPTIONS"])
def query (was, alias, **args):
	# args: q = '', o = 0, f = 10, s = "", w = 30, r = "", l = "en", analyze = 1, data = 1
	if is_json (was.request):
		args = was.request.json ()
	
	q = args.get ("q")
	if not q:
		return error (was.response, "400 Bad Request", 40003, 'parameter q required')
	
	if was.request.command == "delete":
		wissen.get (alias).queue (1, json.dumps ({"query": {'qs': q, 'lang': l, 'analyze': analyze}}))
		return ''
		
	o = args.get ("o", 0)
	f = args.get ("f", 10)
	s = args.get ("s", "")
	w = args.get ("w", 30)
	l = args.get ("l", "en")
	r = args.get ("r", "")
	analyze = args.get ("analyze", 1)
	data = args.get ("data", 1)
	if type (q) is list:
		return was.jstream ([wissen.query (alias, eq, o, f, s, w, r, l, analyze, data, limit = 1) for eq in q])
	return was.jstream (wissen.query (alias, q, o, f, s, w, r, l, analyze, data, limit = 1))

@app.route ("/<alias>/guess", methods = ["GET", "POST", "OPTIONS"])
def guess (was, alias, **args):
	# args: q = '', l = 'en', c = "naivebayes", top = 0, cond = ""
	if is_json (was.request):
		args = was.request.json ()
	q = args.get ("q")
	if not q:
		return error (was.response, "400 Bad Request", 40003, 'parameter q required')
	l = args.get ("l", 'en')
	c = args.get ("c", 'naivebayes')
	top = args.get ("top", 0)
	cond = args.get ("cond", '')
	if type (q) is list:
		return was.jstream ([wissen.guess (alias, eq, l, c, top, cond) for eq in q])
	return was.jstream (wissen.guess (alias, q, l, c, top, cond))
	
@app.route ("/<alias>/cluster", methods = ["GET", "POST", "OPTIONS"])
def cluster (was, alias, **args):
	if is_json (was.request):
		args = was.request.json ()
	q = args.get ("q")
	if not q:
		return error (was.response, "400 Bad Request", 40003, 'parameter q required')
	l = args.get ("l", 'en')	
	if type (q) is list:
		return was.jstream ([wissen.cluster (alias, eq, l) for eq in q])	
	return was.jstream (wissen.cluster (alias, q, l))

