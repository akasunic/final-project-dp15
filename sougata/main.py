#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import feedparser
import logging
import urllib
import json
import time
from webapp2_extras import jinja2

#lets get all the email ids
myEmailId = "senigmatic@gmail.com"
myFriends = ["hxxxxxxxxxxx@gmail.com","sxxxxx.xxxxxx@gmail.com","avixxxxxxxx@gmail.com"]
baseFolder = "E:\\work\\course\\Data Pipeline\\Project 2\\data\\"
months={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
minYear = 2016
maxYear=1900

storeMsg = {}
storeCount={}
storeContent = {}
dataArranged=[]
toWrite="monthYear"
toSendArray = []

def populateData():
	global toSendArray
	toSendArray = []
	logging.info(toSendArray)
	del toSendArray[:]
	for emailId in myFriends:
		storeMsg["From_"+emailId.split('@')[0]]={}
		storeCount["From_"+emailId.split('@')[0]]=0
		storeMsg["To_"+emailId.split('@')[0]]={}
		storeCount["To_"+emailId.split('@')[0]]=0
	
#	logging.info(storeMsg)
	
def getFrequency(word=""):
	global minYear,maxYear
	with open(baseFolder+'dataVis.json') as data_file:    
		data = json.load(data_file)
	for person in myFriends:
		storeContent["From_"+person.split('@')[0]]={}
		storeContent["To_"+person.split('@')[0]]={}
	
	for currData in data:
		try:
			content=currData["content"]	
			if word not in content:
#				logging.info(content)
				continue
			
			mod_date = currData["Date"]
			mod_dateSplit = mod_date.split( )
			mod_dateSplit[2] = months[mod_dateSplit[2]]
			mod_date = mod_dateSplit[3]+'-'+mod_dateSplit[2]#+" "+mod_dateSplit[4]
			mod_date1= mod_dateSplit[3]+""+mod_dateSplit[2]+""+mod_dateSplit[1]
			frmt_time = time.strptime(mod_date, "%Y-%m")
			#print currData["From"],frmt_time
			mod_date=mod_date.encode("utf-8")
	
			if int(minYear)>int(mod_dateSplit[3]):
				minYear = int(mod_dateSplit[3].encode("utf-8"))
			if maxYear<int(mod_dateSplit[3]):
				maxYear=int(mod_dateSplit[3].encode("utf-8"))
			
			
			for person in myFriends:
				if person in currData["From"]:
					#logging.info("Searching for "+word)
					if mod_date in  storeMsg["From_"+person.split('@')[0]]:
						storeMsg["From_"+person.split('@')[0]][mod_date] = storeMsg["From_"+person.split('@')[0]][mod_date] +1
						if word is "":
							storeContent["From_"+person.split('@')[0]][mod_date]=storeContent["From_"+person.split('@')[0]][mod_date]+"\n\n"+str(content.encode("utf-8"))[:50]+"...<HR>"
						else:
							storeContent["From_"+person.split('@')[0]][mod_date]=storeContent["From_"+person.split('@')[0]][mod_date]+"\n\n..."+str(content.encode("utf-8"))[str(content.encode("utf-8")).index(word)-25:str(content.encode("utf-8")).index(word)+25]+"...<HR>"
					else:
						storeMsg["From_"+person.split('@')[0]][mod_date]=1
						
						if word is "":
							storeContent["From_"+person.split('@')[0]][mod_date]=str(content.encode("utf-8"))[:50]+"...<HR>"
						else:
							storeContent["From_"+person.split('@')[0]][mod_date]="..."+str(content.encode("utf-8"))[str(content.encode("utf-8")).index(word)-25:str(content.encode("utf-8")).index(word)+25]+"...<HR>"

					if mod_date == "2006-04":
						logging.info(content)
					

					storeCount["From_"+person.split('@')[0]]=storeCount["From_"+person.split('@')[0]]+1

			if myEmailId in currData["From"]:
				for person in myFriends:	
					if person in currData["To"]:
						if mod_date in  storeMsg["To_"+person.split('@')[0]]:
							storeMsg["To_"+person.split('@')[0]][mod_date] = storeMsg["To_"+person.split('@')[0]][mod_date] +1
							
							if word is "":
								storeContent["To_"+person.split('@')[0]][mod_date]=storeContent["To_"+person.split('@')[0]][mod_date]+"\n\n"+str(content.encode("utf-8"))[:50]+"...<HR>"
							else:
								storeContent["To_"+person.split('@')[0]][mod_date]=storeContent["To_"+person.split('@')[0]][mod_date]+"\n\n..."+str(content.encode("utf-8"))[str(content.encode("utf-8")).index(word)-25:str(content.encode("utf-8")).index(word)+25]+"...<HR>"

						else:
							storeMsg["To_"+person.split('@')[0]][mod_date]=1
							
							if word is "":
								storeContent["To_"+person.split('@')[0]][mod_date]=str(content.encode("utf-8"))[:50]+"...<HR>"
							else:
								storeContent["To_"+person.split('@')[0]][mod_date]="..."+str(content.encode("utf-8"))[str(content.encode("utf-8")).index(word)-25:str(content.encode("utf-8")).index(word)+25]+"...<HR>"


			 			storeCount["To_"+person.split('@')[0]]=storeCount["To_"+person.split('@')[0]]+1
			#logging.info(storeContent)
		except Exception as detail:
			#logging.info(detail)	
			continue
#	logging.info(storeMsg)
#	logging.info(storeCount)
	
#	logging.info(minYear)
#	logging.info(maxYear)
	
	
def fillMissingDates():
	global toWrite
	#print minYear,"---",maxYear
	headerCreated=0
	for ii in range(minYear,maxYear+1):
		for jj in range(1,13):
			dictData = {}
			
			strVal = ""
			if jj<10:
				strVal = str(ii)+"-0"+str(jj)
			else:
				strVal = str(ii)+"-"+str(jj)
#			logging.info(strVal)
			for exchange in storeMsg:
				if headerCreated is 0:
					toWrite=toWrite+","+exchange[:exchange.index('_')+3]
				if strVal in storeMsg[exchange]:
					try:
						dictData[strVal]=dictData[strVal]+","+str(storeMsg[exchange][strVal])#=storeMsg[exchange[strVal]]+","+str(exchange[strVal])
					except:
					#	print storeMsg[exchange][strVal]
						dictData[strVal]=str(storeMsg[exchange][strVal])
				else:
					try:
						dictData[strVal]=str(dictData[strVal])+",0"
					except:
						dictData[strVal]="0"
			headerCreated=1
			toWrite=toWrite+"\n"+strVal+","+str(dictData[strVal])
			#print dictData
					
			dataArranged.append(dictData)		
	#print baseFolder+'testWrite.csv'
	#f = open(baseFolder+'testWrite.csv', 'w')
	#f.write(toWrite)
#	logging.info(toWrite)

def toSend():
	splitted = toWrite.split('\n')
	splitHead = splitted[0].split(',')
	first=0
	for data in splitted:
		toPush = {}
		
		if first is 0:
			first=1
			continue
		splitData = data.split(',')
		ages = []
		for dataS in range(0,len(splitData)):
			if dataS>len(splitHead)-1:
				break
			if dataS is not 0:
				TempVal = {}
				TempVal['name'] = str(splitHead[dataS])
				TempVal['value'] = int(splitData[dataS])
				ages.append(TempVal)
			tempStore = splitHead[dataS]+":"+splitData[dataS]
			tempPush={}
			if splitHead[dataS].startswith('From'):
				toPush[splitHead[dataS]] = splitData[dataS]
			else:
				toPush[splitHead[dataS]] = splitData[dataS]#"-"+splitData[dataS]
		#toPush['ages']=ages
		toSendArray.append(toPush)
	

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)
    def render_response(self, _template, **context):
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


class MainHandler(BaseHandler):
    def get(self):
    	global dataArranged,toSendArray,storeContent,toWrite
    	
    	storeContent = {}
	dataArranged=[]
	toSendArray = []
	toWrite="monthYear"

    	
    	populateData()
    	getFrequency()
    	fillMissingDates()
    	toSend()
    	toWrite1 = []
    	tempList = {}
    	tempList['toWrite'] = toWrite
    	toWrite1.append(tempList)
    	
    	context = {"frequency":dataArranged,"toWrite":toWrite1,"toSend":toSendArray,"content":storeContent}
    	logging.info(context)

        self.render_response('index.html', **context)
        
    def post(self):
        word= self.request.get('searchWord')
        
        global dataArranged,toSendArray,storeContent,toWrite
	    	
	storeContent = {}
	dataArranged=[]
	toSendArray = []
	toWrite="monthYear"

        
    	populateData()
    	getFrequency(word)
    	fillMissingDates()
    	toSend()
    	context = {"frequency":dataArranged,"toSend":toSendArray,"content":storeContent}
	logging.info(context)
        self.render_response('index.html', **context)

    

app = webapp2.WSGIApplication([('/.*', MainHandler)], debug=True)
