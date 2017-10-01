import urllib.request, urllib.error, urllib.parse
import json
from os import stat, getenv, makedirs
from os.path import basename, isdir, isfile
import configparser
import os, requests, sys
from pathlib import Path

from click.commands import info

appsEndpoint = "https://open.uappexplorer.com/api/apps"
manageEndpoint = "https://open.uappexplorer.com/api/v1/manage/apps"
revisionEndpoint = "https://open.uappexplorer.com/api/v2/apps/revision"

# Taken from: http://code.activestate.com/recipes/577058/
def query_yes_no(question, default="yes"):
	valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

class repo:
	def __init__(self):
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
			return

		if not isdir(getenv("HOME")+"/.openstorecli"):
			makedirs(getenv("HOME")+"/.openstorecli")
		if not isfile(getenv("HOME")+"/.openstorecli/conf.conf"):
			self.saveConfig()
		else:
			conf.read(getenv("HOME")+"/.openstorecli/conf.conf")
			self.api = conf.get("Repo", "API")

	def saveConfig(self):
		conf = configparser.ConfigParser()
		self.conf = conf
		cfgfile = open(getenv("HOME")+"/.openstorecli/conf.conf",'w')
		conf.add_section('Repo')
		conf.set('Repo','API', self.api)
		conf.write(cfgfile)
		cfgfile.close()

	def hasApi(self):
		if self.api == "": return False
		else: return True

	def upload(self, fil, _force_yes = False):
		self.click = click.commands.info.get_manifest(object(), str(Path(fil).resolve()))
		print ("Package id:", self.click["name"])

		if not _force_yes:
			if not query_yes_no("Do you confirm you want to upload the package?"):
				print("Aborted")
				return


		if not self.isNewerVersion(self.click["name"], self.click["version"]):
			print("There is already a revision with the same version. Aborting...")
			return

		self._id=self.click["name"]
		files = {'file': open(fil, 'rb')}

		url = manageEndpoint + "/" + self._id + "/?apikey=" + self.api
		
		r=requests.put(url, files=files)

		print ("Successfully uploaded " + self._id)

	# OK
	def update_info(self, _id, _force_yes = False):
		if not self.idExistWithAuth(_id):
			raise ValueError("The id %s does not exist on the server", self.click["name"])

		if not self.update == "":
			print ("\nSummary of the information provided for package:", _id)
			for x in self.update:
				print (str(x).ljust(15), ':', self.update[x])

		if not _force_yes:
			if not query_yes_no("Do you confirm you want to update remote info?"):
				print("Aborted")
				return

		url = manageEndpoint + "/" + _id + "?apikey=" + self.api

		r=requests.put(url, data=self.update)

		if r.status_code == 404:
			print ("Failed to update info. Please ensure pkg_id is valid.")
		elif r.status_code == 400:
			print ("There was an error updating the info.")
			print ("Error info:", r.text)
		else:
			print ("Successfully updated remote package info")

	def search(self, _query):
		url = appsEndpoint + "?search=" + str(_query)
		with urllib.request.urlopen(url) as response:
			return json.loads(response.read().decode("utf-8"))

	def info(self, _id):
		url = appsEndpoint + "/" + str(_id)
		with urllib.request.urlopen(url) as response:
			return json.loads(response.read().decode("utf-8"))

	def infoWithAuth(self, _id):
		url = manageEndpoint + "/" + str(_id) + "/?apikey=" + self.api
		with urllib.request.urlopen(url) as response:
			return json.loads(response.read().decode("utf-8"))

	def idExistWithAuth(self, _id):
		i = self.infoWithAuth(_id)["data"]
		if i["id"] == _id:
			return True
		return False

	def isNewerVersion(self, idd, version):
		i = self.infoWithAuth(idd)["data"]
		revAlreadyExists = False
		
		revisions = i["revisions"]

		for r in revisions:
			if r["version"] == version: revAlreadyExists = True

		if revAlreadyExists:
			return False
		else:
			return True
