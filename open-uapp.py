#!/usr/bin/env python

import sys
import os
import shutil
import openUapp

uApp = openUapp.repo()
uAppLocal = openUapp.local()

if sys.argv[1] == "update":
	if sys.argv[2] and sys.argv[2] != "":
		arggs = argv[2]
		arggs.split(",")
		values= argv[3]
		values.split(",")
		gotOne=False
		i=0
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
				print "The key: " + argg + " do not exsist in the repo, ignoring"			
			i+=1
		if gotOne:
			uApp.update()
		else:
			usage()
	else:
		usage()
				
elif sys.argv[1] == "delete":
	if sys.argv[2] and sys.argv[2] != "":
		if uApp.idExists(sys.argv[2]):
			uApp.delete(uApp.get_idFromid(sys.argv[2]))
			print "Deleted: " + sys.argv[2]
		else:
			print "The id " + sys.argv[2] + " do not exsist!"
	else:
		usage()
		
elif sys.argv[1] == "new" or sys.argv[1] == "add":
	print "under deveopment"
		 
elif sys.argv[1] == "loaclupdate":
	print "under deveopment"
"""	arggs = argv[2]
	arggs.split(",")
	for argg in arggs:
		if argg == "version":
				#Dothis
		elif argg == "pakage":
				#DoThis
		elif argg == "name":
				#DoThis
		elif argg == "license":
				#DoThis
		elif argg == "tagline":
				#DoThis
		elif argg == "source":
				#DoThis
		elif argg == "icon":
				#DoThis
		elif argg == "description":
				#DoThis
		else:
			print "The key: " + argg + " do not exsist in the repo, ignoring" """

	
def usage():
	print "Usage:"
