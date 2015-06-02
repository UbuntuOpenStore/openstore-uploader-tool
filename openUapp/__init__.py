import urllib2, urllib, json
from os import stat, getenv, makedirs
from os.path import basename, isdir, isfile
import ConfigParser
import requests

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
		self.repoUrl="https://open.uappexplorer.com/api/apps" 
		self.local=False
		self.debug=False
		self.repo=""
		self.update={}
		self.api=""
		self.smartApi=""
		self.smartPass=""
		self.loadConfig()
		
	def loadConfig(self):
		conf = ConfigParser.ConfigParser()
		self.conf = conf
		if not isdir(getenv("HOME")+"/.openuapp"):
			makedirs(getenv("HOME")+"/.openuapp")
		if not isfile(getenv("HOME")+"/.openuapp/conf.conf"):
			self.saveConfig()
		else:
			conf.read(getenv("HOME")+"/.openuapp/conf.conf")
			self.repoUrl = conf.get("Repo", "repoUrl")
			self.api = conf.get("Repo", "API")
			self.smartApi = conf.get("SmartFile", "API")
			self.smartPass = conf.get("SmartFile", "Pass")
			
	def saveConfig(self):
		conf = ConfigParser.ConfigParser()
		self.conf = conf
		cfgfile = open(getenv("HOME")+"/.openuapp/conf.conf",'w')
		conf.add_section('Repo')
		conf.set('Repo','repoUrl', self.repoUrl)
		conf.set('Repo','API', self.api)
		conf.add_section('SmartFile')
		conf.set('SmartFile','API', self.smartApi)
		conf.set('SmartFile','Pass', self.smartPass)
		conf.write(cfgfile)
		cfgfile.close()
		
	def hasApi(self):
		if self.api == "": return False
		else: return True
		
	def updateR(self):
		url = self.repoUrl + "?apikey=" + self.api
		requests.put(url, data=self.update)
		
	def new(self):
		self.update["apikey"] = self.api
		values = urllib.urlencode(self.update)
		req = urllib2.Request(self.repoUrl, values)
		urllib2.urlopen(req).read()
		
	def delete(self, _id):
		url = self.repoUrl + "?apikey=" + self.api
		data = {}
		data["_id"] = _id
		requests.delete(url, data=data)
				
	def get(self):
		try: self.repo = json.loads(urllib2.urlopen(self.repoUrl).read())
		except:
			print "Cannot fetch repo from url: " + self.repoUrl
			raise
		
	def smartApiExist(self):
		if self.smartApi == "" and self.smartPass == "": return False
		else: return True	
			
	def upload(self, fil, icon=False):
		from smartfile import BasicClient
		filename = basename(fil)
		filee = file(fil, 'rb')
		api = BasicClient(self.smartApi, self.smartPass)
		response = api.post('/path/data/openappstore/v1/', file=filee)
		if self.debug: print "debug: "+response
		if self.debug: print 'debug: https://file.ac/w-fprv1yrTM/' + filename
		if not icon: 
			self.update["package"] = 'https://file.ac/w-fprv1yrTM/' + filename  
			self.update["size"] = stat(fil).st_size
		else: self.update["icon"] = 'https://file.ac/w-fprv1yrTM/' + filename
		
	def idExist(self, idd):
		if self.repo == "":
			self.get()
		print idd
		for i in self.repo["data"]:
			print i["id"]
			if i["id"] == idd:
				print "yeah?"
				return True
		print "False?"
		return False
		
	def get_idFromid(self, idd):
		if self.repo == "":
			self.get()
		for i in self.repo["data"]:
			if i["id"] == idd:
				return i['_id']
		return ""
	

