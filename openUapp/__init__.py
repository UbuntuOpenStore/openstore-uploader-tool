import urllib2, urllib, json
from os import stat, getenv, makedirs
from os.path import basename, isdir, isfile
import ConfigParser
import requests
import os
import tarfile

class local:
	def __init__(self):
		self.localFile="test/repolist.json"
		self.debug=False
		self.repoJson=""
		self.repo=""
		self.click=""
	
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
		self.click=""
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
		
	def updateR(self, fil):
		if not os.path.isfile(fil):
			raise Exception("%s does not exist", fil)
		self.readClick(fil)
		if not self.idExist(self.click["name"]):
			raise ValueError("The id %s does not exist on the server", self.click["name"])
		files = {'file': open(fil, 'rb')}
		url = self.repoUrl+"/"+self.click["name"]+"/?apikey=" + self.api
		try:
			if self.update == "":				
				r=requests.put(url, files=files)
			else:
				r=requests.put(url, files=files, data=self.update)
			print r
		except: raise ValueError("Faled to connect to the server or the server returned with an error")
		
	def new(self, fil):
		if not os.path.isfile(fil):
			raise ValueError("%s does not exist", fil)
		files = {'file': open(fil, 'rb')}
		url = self.repoUrl + "?apikey=" + self.api
		try: 
			if self.update == "":
				r=requests.post(url, files=files)
			else:
				r=requests.post(url, files=files, data=self.update)
			print r
		except: raise ValueError("Faled to connect to the server or the server returned with an error")
		
	def delete(self, _id):
		if not self.idExist(_id):
			raise ValueError("The id %s does not exit...", _id)
		url = self.repoUrl+"/"+_id+"/?apikey=" + self.api
		try: requests.delete(url)
		except: raise ValueError("Faled to connect to the server or the server returned with an error")
				
	def fetch(self):
		try: self.repo = json.loads(urllib2.urlopen(self.repoUrl).read())
		except: raise ValueError("Cannot fetch repo from url: %s", self.repoUrl)
			
	def getNameFromId(self, _id):
		if not self.idExist(_id):
			raise ValueError("The id %s does not exit...", _id)
		for i in self.repo["data"]:
			if i["id"] == idd:
				return i["name"]
		return "Null"

	def idExist(self, idd):
		if self.repo == "":
			self.fetch()
		for i in self.repo["data"]:
			if i["id"] == idd:
				return True
		return False
		
	def readClick(self, fil):
		cdback = os.getcwd()
		os.chdir("/tmp")
		os.system("mkdir uapp")
		os.chdir(cdback)
		os.system("cp "+fil+" /tmp/uapp/o.click")
		os.chdir("/tmp/uapp")
		os.system("ar vx o.click")
		tar = tarfile.open("control.tar.gz")
		f=tar.extractfile(tar.getmember("./manifest"))
		self.click = json.loads(f.read())
		os.system("rm -r /tmp/uapp")
		os.chdir(cdback)
		
