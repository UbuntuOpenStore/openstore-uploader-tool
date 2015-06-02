import urllib2, urllib, json
from os import stat
from os.path import basename

class local:
	def __init__(self):
		self.localFile="test/repolist.json"
		self.debug=False
		self.repoJson=""
		self.repo=""
	
	def localUpdateJson(appID, name, value):
		r = self.repoJson
		b = []
		e = {}
		for i in r["data"]:
			if i["id"] == appID:
				i[name] = value
			b.append(i)
		e["data"] = b
		self.repo = e
		
	def openFile(self):
		f = open(self.localFile, "r")
		return f.read()
	
	def writeFile(self):
		self.repoJson = json.dumps(self.repo)
		f = open(self.localFile, "w")
		f.write(self.repoJson)
		
class repo:
	def __init__(self):
		self.localFile="test/repolist.json"
		self.repoUrl="https://open.uappexplorer.com/api/apps" 
		self.local=False
		self.debug=False
		self.repo=""
		self.update={}
		self.api=""
	
	def hasApi(self):
		if self.api == "": return False
		else: return True
		
	def update(self):
		url = self.repoUrl + "?apikey=" + self.api
		build = urllib2.build_opener(urllib2.HTTPHandler)
		values = urllib.urlencode(self.update)
		req = urllib2.Request(url, values)
		req = get_method = lambda: 'PUT'
		build.open(req)
		
	def new(self):
		self.update["apikey"] = self.api
		values = urllib2.urlencode(self.update)
		req = urllib2.Request(self.repoUrl, values)
		urllib2.urlopen(req).read()
		
	def delete(self, _id):
		url = self.repoUrl + "?apikey=" + self.api
		data = {}
		data["_id"] = _id
		build = urllib2.build_opener(urllib2.HTTPHandler)
		value = urllib.urlencode(data)
		req = urllib2.Request(url, value)
		req = get_method = lambda: 'DELETE'
		build.open(req)
				
	def get(self):
		try: self.repo = json.loads(urllib2.urlopen(self.repoUrl).read())
		except:
			print "Cannot fetch repo from url: " + self.repoUrl
			raise
			
	def upload(self, fil, icon=False):
		#from smartfile import BasicClient
		filename = basename(fil)
		filee = file(fil, 'rb')
		#api = BasicClient()
		#response = api.post('/path/data/openappstore/v1/', file=filee)
		if self.debug: print "debug: "+response
		if self.debug: print 'debug: https://file.ac/w-fprv1yrTM/' + filename
		if not icon: 
			self.update["package"] = 'https://file.ac/w-fprv1yrTM/' + filename  
			self.update["size"] = stat(fil).st_size
		else: self.update["icon"] = 'https://file.ac/w-fprv1yrTM/' + filename
		
	def idExist(self, idd):
		if self.repo == "":
			self.get()
		for i in self.repo["data"]:
			if i["id"] == idd:
				return True
		return False
		
	def get_idFromid(self, idd):
		if self.repo == "":
			self.get()
		for i in self.repo["data"]:
			if i["id"] == idd:
				return i['_id']
		return ""
	

