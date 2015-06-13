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
			
	def saveConfig(self):
		conf = ConfigParser.ConfigParser()
		self.conf = conf
		cfgfile = open(getenv("HOME")+"/.openuapp/conf.conf",'w')
		conf.add_section('Repo')
		conf.set('Repo','repoUrl', self.repoUrl)
		conf.set('Repo','API', self.api)
		conf.write(cfgfile)
		cfgfile.close()
		
	def hasApi(self):
		if self.api == "": return False
		else: return True
		
	def updateR(self, fil, _id):
		if not os.path.isfile(fil):
			raise ValueError("%s does not exist", fil)
		files = {'file': open(fil, 'rb')}
		url = self.repoUrl+"/"+_id+"/?apikey=" + self.api
		requests.put(url, files=files)
		
	def new(self, fil):
		if not os.path.isfile(fil):
			raise ValueError("%s does not exist", fil)
		files = {'file': open(fil, 'rb')}
		url = self.repoUrl + "?apikey=" + self.api
		requests.post(url, files=files)
		
	def delete(self, _id):
		url = self.repoUrl+"/"+_id+"/?apikey=" + self.api
		requests.delete(url)
				
	def get(self):
		try: self.repo = json.loads(urllib2.urlopen(self.repoUrl).read())
		except:
			print "Cannot fetch repo from url: " + self.repoUrl
			raise
			
	def get(self, idd):
		if self.repo == "":
			self.get()
		for i in self.repo["data"]:
			if i["id"] == idd:
				return i["name"]
		return "Not Found"

	def idExist(self, idd):
		if self.repo == "":
			self.get()
		for i in self.repo["data"]:
			if i["id"] == idd:
				return True
		return False
