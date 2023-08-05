import requests
import queue
import os
import wissen
from wissen import filesystem
from wissen.lib import pathtool, logger as loggerlib
import threading, time
import socket, json

mirror_server = None
DUPLICATE_LOCK = "duplicate-%s" % socket.getfqdn ()
DEBUG = True

def normpath (d):
	d = d.replace ("\\", "/")
	if DEBUG:
		d = d.replace ('D:/apps/', 'd:/var/')
	return d

DOWNLOAD_FAILDS = {}
def download (tque):
	global mirror_server, DOWNLOAD_FAILDS
	
	while 1:
		item = tque.get ()
		if item is None:
			break
		col, entity, group, fn, savepath	= item
		pathtool.mkdir (os.path.split (savepath)[0])
		url = "%s/%s/%s/%s/%s" % (mirror_server, col, entity, group, fn)		
		surl = "/%s/%s/%s/%s" % (col, entity, group, fn)		
		logger ("downloading from %s" % url)
		
		response = requests.get(url, stream=True)
		cl = int (response.headers ["Content-Length"])						
		rl = 0
		
		if not response.ok:
			logger ("download failed  HTTP %d: %s" % (response.status_code, url), 'fail')
			DOWNLOAD_FAILDS [col] = None
			continue
		
		with open(savepath, 'wb') as handle:
			if cl:
				for block in response.iter_content(1024):
					rl += len (block)
					if rl % 1024000 == 0:
						logger ("%d%% downloaded %s" % (rl/cl * 100, surl))
					handle.write(block)				
				logger ("%d%% downloaded %s" % (rl/cl * 100, surl))
				if rl != cl:
					logger ("incomplete download: %s" % url, 'fail')
					DOWNLOAD_FAILDS [col] = None
					

def remove_end_slash (url):
	while url:
		if url [-1] != "/":
			return url
		url = mirror_server [:-1]	
			
def mirror (origin, local):
	global mirror_server, DOWNLOAD_FAILDS
	
	mirror_server = remove_end_slash (origin)
	local_server = local and remove_end_slash (local) or None
	
	r = requests.get ("%s/" % mirror_server)
	for col in r.json () ["collections"]:		
		logger ("%s mirroring started" % col)
		requests.post ("%s/%s/locks/%s" % (mirror_server, col, DUPLICATE_LOCK))
		r = requests.get ("%s/%s" % (mirror_server, col))
		status = r.json ()
		valid_segments = [seginfo [0] for seginfo in status ['segmentinfos']]
		keep_going = True		
		for name, ctime in status ["locks"]:
			if name == "index":
				keep_going = False
				break
		
		if not keep_going:
			requests.delete ("%s/%s/locks/%s" % (mirror_server, col, DUPLICATE_LOCK))
			continue
		
		for d in status ['indexdirs']:
			pathtool.mkdir (normpath (d))
		
		que = []
		new_file = False
		for group in status ["segmentfiles"]:
			segs = status ["segmentfiles"][group]			
			if 'segments' in segs:
				sfn = segs.pop ('segments')[0]
				dfn = normpath (sfn)
				if group == "primary":
					que.append ((col, 'collection', group, "segments", dfn + ".new"))
				else:
					que.insert (0, (col, 'collection', group, "segments", dfn))
			
			for seg, files in segs.items ():
				if group == "primary" and int (seg) not in valid_segments:
					continue					
				for sfn, ssize, smtime in files:
					dfn = normpath (sfn)
					if not os.path.isfile (dfn):
						que.insert (0, (col, 'segments', group, str(seg) + sfn [-4:], dfn))
						new_file = True
					else:	
						dmtime = os.path.getmtime (dfn)
						dsize = os.path.getsize (dfn)
						if dsize != ssize or smtime > dmtime:
							que.insert (0, (col, 'segments', group, str (seg) + sfn [-4:], dfn))
							new_file = True
			
		if not new_file:			
			logger ("no changes in %s" % col)
		
		else:	
			tque = queue.Queue ()		
			for item in que:
				#col, entity, group, fn, savepath
				logger ("queuing %s %s %s %s %s" % item)
				tque.put (item)
			for i in range (2):	
				tque.put (None)		
			
			for i in range (2):
				t = threading.Thread (target = download, args = (tque,))
				t.start ()
			
			while threading.activeCount () > 1:				
				time.sleep (1)
			
			if col in DOWNLOAD_FAILDS:
				logger ("%s mirror failed, maybe mext time" % col, "fail")
				continue
				
			segments = os.path.join (normpath (status ['indexdirs'][0]), 'segments.new')
			if os.path.isfile (segments [:-4]):
				os.remove (segments [:-4])

			os.rename (segments, segments[:-4])
				
		requests.delete ("%s/%s/locks/%s" % (mirror_server, col, DUPLICATE_LOCK))
		logger ("%s mirroring complete" % col)
		
		logger ("download configuration %s" % col)	
		colopt = status ["colopt"]
		dcolopt = normpath (colopt ['path'])
		if not os.path.isfile (dcolopt):
			requests.post ("%s/%s" % (local_server, col), json.dumps (colopt ['data']))
			logger ("registering new collection %s" % col)
		elif colopt ["mtime"] > os.path.getmtime (dcolopt) or colopt ["size"] != os.path.getsize (dcolopt):
			requests.patch ("%s/%s" % (local_server, col), json.dumps (colopt ['data']))
			logger ("patch collection %s" % col)
		
	logger ("syncing collections")
	origin_side = requests.get ("%s/" % mirror_server).json () ["collections"]
	for col in requests.get ("%s/" % local_server).json () ["collections"]:
		if col not in origin_side:
			requests.delete ("%s/%s?side_effect=data" % (local_server, col))
			logger ("collection %s has been removed" % col)
	
	if DOWNLOAD_FAILDS:
		logger ("clollections %s mirror failed" % ",".join (list (DOWNLOAD_FAILDS.keys ())), "fail")
		
		
if __name__ == "__main__":
	import sys, getopt
	
	logger = loggerlib.screen_logger ()
	argopt = getopt.getopt(sys.argv[1:], "l:", ["log="])
	for k, v in argopt [0]:
		if k == "-l" or k == "--log":			
			logger = loggerlib.multi_logger ([logger, loggerlib.rotate_logger (v, "wissen", "daily")])
	
	local = None
	if len (argopt [1])	 == 2:
		origin, local = tuple (argopt [1])
	elif len (argopt [1])	 == 1:
		origin = argopt [1][0]		
	else:	
		print ('Usage: mirror.py origin local')
		print ('  ex. mirror.py  http://192.168.1.200:5000/v1 http://192.168.1.1:5000/v1')
		sys.exit ()	

	mirror (origin, local)
	