#!/usr/bin/env python

import sys
import os
import shutil
import openUapp
from os.path import isfile

uApp = openUapp.repo()
uAppLocal = openUapp.local()

def usage():
	print 'Usage:'	
	print 'open-uapp update [app ID] [keys splited by ,] "[values splited by , (in the same order as keys)]" | Edit an app'
	print 'open-uapp new | Create a new app'
	print 'open-uapp delete [app ID] | Delete an App'
	print 'open-uapp list | List all Apps'
	print 'open-uapp info [app ID] Displays info about an App'
	print ' '
	print 'Examples:'
	print 'open-uapp update openstore.mzanetti name,version,pakage "testapp,0.1,build/package"'
	print 'open-uapp new'
	print 'open-uapp delete openstore.mzanetti'
	print 'open-uapp list'
	print 'open-uapp info openstore.mzanetti'
	
	sys.exit()

if len(sys.argv) <= 1:
	usage()
elif sys.argv[1] == "keys":
	print "version, package, name, license, soucre, icon, description, author, category"
elif sys.argv[1] == "update":
	if len(sys.argv) > 2:
		if not uApp.hasApi():
			print "You have not provided a API key"
			sys.exit()
		if not uApp.idExist(sys.argv):
			print "The ID " + sys.argv[2] + " does not exsist"
			sys.exit()
		uApp.update["_id"] = uApp.get_idFromid(sys.argv[2])
		arggs=sys.argv[3].split(",")
		values=sys.argv[4].split(",")
		gotOne=False
		i=0
		print arggs
		for argg in arggs:
			if argg == "version":
				uApp.update["version"] = values[i] 
				gotOne=True
			elif argg == "package":
				if os.path.isfile(values[i]):
					uApp.upload(values[i])
					gotOne=True
				else:
					print "The file " + values[i] + " do not exsist"  
					sys.exit()
			elif argg == "name":
				uApp.update["name"] = values[i] 
				gotOne=True
			elif argg == "license":
				uApp.update["license"] = values[i] 
				gotOne=True
			elif argg == "tagline":
				uApp.update["tagline"] = values[i] 
				gotOne=True
			elif argg == "source":
				uApp.update["source"] = values[i] 
				gotOne=True
			elif argg == "icon":
				if os.path.isfile(values[i]):
					uApp.upload(values[i], True)
					gotOne=True
				else:
					print "The file " + values[i] + " do not exsist"  
					sys.exit()
			elif argg == "description":
				uApp.update["description"] = values[i] 
				gotOne=True
			elif argg == "author":
				uApp.update["author"] = values[i] 
				gotOne=True
			elif argg == "category":
				uApp.update["category"] = values[i] 
				gotOne=True			
			else:
				print "The key '" + argg + "' do not exsist, ignoring"			
			i+=1
		if gotOne:
			print " "
			print "After:"
			print uApp.update
			#uApp.update()
		else:
			usage()
	else:
		usage()
				
elif sys.argv[1] == "delete":
	if len(sys.argv) > 2:
		if not uApp.hasApi():
			print "You have not provided a API key"
			sys.exit()
		if uApp.idExist(sys.argv[2]):
			uApp.delete(uApp.get_idFromid(sys.argv[2]))
			print "Deleted: " + sys.argv[2]
		else:
			print "The id " + sys.argv[2] + " do not exsist!"
	else:
		usage()
		
elif sys.argv[1] == "new" or sys.argv[1] == "add":
	if not uApp.hasApi:
		print "You have not provided a API key"
		sys.exit()
	uApp.update["author"] = raw_input("Author:")
	uApp.update["category"] = raw_input("Category:")
	uApp.update["description"] = raw_input("Description:")
	icon = raw_input("Icon (file):")
	while not os.path.isfile(icon):
		print "The file " + icon + " do not exsist try agian"
		pack = raw_input("Icon (file):")
	uApp.upload(icon, True)
	#TODO: Check if idExist
	uApp.update["id"] = raw_input("ID:")
	uApp.update["license"] = raw_input("License:")
	uApp.update["name"] = raw_input("Name:")
	pack = raw_input("Package (file):")
	while not os.path.isfile(pack):
		print "The file " + pack + " do not exsist try agian"
		pack = raw_input("Package (file):")
	uApp.upload(pack)
	uApp.update["source"] = raw_input("Source:")
	uApp.update["tagline"] = raw_input("Tagline:")
	uApp.new()
		 
elif sys.argv[1] == "list":
	uApp.get()
	for i in uApp.repo["data"]:
		print i["name"] + " | " + i["id"]
		
elif sys.argv[1] == "info":
	if len(sys.argv) > 2:
		uApp.get()
		notFound=True
		for i in uApp.repo["data"]:
			if sys.argv[2] == i["id"]:
				notFound=False
				print "Name: " + i["name"]
				print "Description: " + i["description"]
				print "Tagline: " + i["tagline"]
				print "License: " + i["license"]
				print "Author: " + i["author"]
				print "Category: " + i["category"]
		if (notFound): print "Cannot find app with a id: " + sys.argv[2]
	else:
		print "Missing appID argument"
	
elif sys.argv[1] == "loaclupdate":
	print "under deveopment"

else:
	usage()
