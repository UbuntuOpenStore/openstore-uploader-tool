#!/usr/bin/env python

import sys
import os
import shutil
import openUapp

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
elif sys.argv[1] == "update":
	if len(sys.argv) <= 2:
		arggs=sys.argv[3].split(",")
		values=sys.argv[4].split(",")
		gotOne=False
		i=0
		print arggs
		for argg in arggs:
			if argg == "version":
				uApp.update["version"] = values[i] 
				gotOne=True
			elif argg == "pakage":
				#TODO: FILE CHEKCK IF EXSISTS FIRST
				uApp.upload(values[i])
				gotOne=True
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
				uApp.upload(values[i], True)
				gotOne=True
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
				print "The key '" + argg + "' do not exsist in the repo, ignoring"			
			i+=1
		if gotOne:
			print "YEAH"
			#uApp.update()
		else:
			usage()
	else:
		usage()
				
elif sys.argv[1] == "delete":
	if len(sys.argv) <= 2:
		if uApp.idExists(sys.argv[2]):
			uApp.delete(uApp.get_idFromid(sys.argv[2]))
			print "Deleted: " + sys.argv[2]
		else:
			print "The id " + sys.argv[2] + " do not exsist!"
	else:
		usage()
		
elif sys.argv[1] == "new" or sys.argv[1] == "add":
	print "under deveopment"
		 
elif sys.argv[1] == "list":
	uApp.get()
	for i in uApp.repo["data"]:
		print i["name"] + " | " + i["id"]
		
elif sys.argv[1] == "info":
	if len(sys.argv) <= 2:
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
	
elif sys.argv[1] == "loaclupdate":
	print "under deveopment"

else:
	usage()
