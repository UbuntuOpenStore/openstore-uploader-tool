import urllib.request, urllib.error, urllib.parse
import json
from os import stat, getenv, makedirs
from os.path import basename, isdir, isfile
import configparser
import shutil, tarfile, os, requests

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
		self._id=""
		self.loadConfig()

	def loadConfig(self):
		conf = configparser.ConfigParser()
		self.conf = conf

		if 'OPENSTORE_API_KEY' in os.environ:
			self.api = os.environ.get('OPENSTORE_API_KEY', '')
			self.repoUrl = os.environ.get('OPENSTORE_REPO_URL', '')
			return

		if not isdir(getenv("HOME")+"/.openuapp"):
			makedirs(getenv("HOME")+"/.openuapp")
		if not isfile(getenv("HOME")+"/.openuapp/conf.conf"):
			self.saveConfig()
		else:
			conf.read(getenv("HOME")+"/.openuapp/conf.conf")
			self.repoUrl = conf.get("Repo", "repoUrl")
			self.api = conf.get("Repo", "API")

	def saveConfig(self):
		conf = configparser.ConfigParser()
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

	def updateR(self, fil, force=False):
		isFile=True
		if not os.path.isfile(fil):
			if not self.idExist(fil):
				raise Exception("%s does not exist", fil)
			isFile=False
			self._id=fil
		if isFile:
			self.readClick(fil)
			if not self.idExist(self.click["name"]):
				raise ValueError("The id %s does not exist on the server", self.click["name"])
			if not self.isNeverVersion(self.click["name"], self.click["version"]):
				if force:
					print("There is a never or equal version already published, but pushing as you wanted")
				else:
					raise ValueError("These is a never or equal version already published, use --force to push anyway")
			self._id=self.click["name"]
			files = {'file': open(fil, 'rb')}
		url = self.repoUrl+"/"+self._id+"/?apikey=" + self.api
		
		if self.update == "" and isFile:
			r=requests.put(url, files=files)
		elif not isFile:
			r=requests.put(url, data=self.update)
		else:
			r=requests.put(url, files=files, data=self.update)

	def new(self, fil):
		if not os.path.isfile(fil):
			raise ValueError("%s does not exist", fil)
		files = {'file': open(fil, 'rb')}
		url = self.repoUrl + "?apikey=" + self.api

		if self.update == "":
			r=requests.post(url, files=files)
		else:
			r=requests.post(url, files=files, data=self.update)

	def delete(self, _id):
		if not self.idExist(_id):
			raise ValueError("The id %s does not exit...", _id)
		url = self.repoUrl+"/"+_id+"/?apikey=" + self.api
		requests.delete(url)

	def fetch(self):
		with urllib.request.urlopen(self.repoUrl) as response:
			self.repo = json.loads(response.read().decode("utf-8"))

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

	def isNeverVersion(self, idd, version):
		if self.repo == "":
			self.fetch()
		for i in self.repo["data"]:
			if i["id"] == idd:
				if i["version"].replace(".", "") < version.replace(".", ""):
					return True
		return False

	def readClick(self, fil):
		cdback = os.getcwd()
		os.chdir("/tmp")
		os.makedirs("uapp")
		os.chdir(cdback)
		shutil.copyfile(fil, "/tmp/uapp/o.click")
		os.chdir("/tmp/uapp")
		os.system("ar vx o.click > /dev/null 2>&1")
		tar = tarfile.open("control.tar.gz")
		f=tar.extractfile(tar.getmember("./manifest"))
		self.click = json.loads(f.read().decode("utf-8"))
		os.system("rm -r /tmp/uapp")
		os.chdir(cdback)
