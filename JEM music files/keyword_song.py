# -*- coding: utf-8-sig -*-
'''This script must be run from JEM, Jython Environment for Music
It can be downloaded here: http://www.cs.cofc.edu/~manaris/jythonmusic/
Site also includes tutorials and sample code
This script is using ideas and starting code from guidoWordMusic.py

This script takes as input a json file representing an email communication between 2 friends, 
which for this project was created using parse_mbox.py.
It then sets rules to assign notes to vowels,
and different pitches (lower/higher) to each friend so we can distinguish.
The tempo is a factor of both the gap length and the verbosity of the emails.
In other words, slower tempos indicate less frequent and verbose communication.

This script can be modified to allow the music to convey other aspects of the relationship.
'''


from music import *
from string import *
import json
from datetime import datetime, timedelta

#MUSICAL FOUNDATION SET UP
# Creates a melody from text using the following rules:
#
# 1) Vowels specify pentatonic pitch, 'a' is C4, 'e' is D4, 
#    'i' is E4, 'o' is G4, and 'u' is A4.
#
# 2) Consonants extend the duration of the previous note (if any).

#----------------Your data here--------------
json_file = ''#string representing location of json file to sonify

# define keywords, will later match with corresponding musical pitches and person writing email
#examples are given 
keywords       = ["rent", "good", "!"]

#String representing first names (or parts of first names) as they appear in email
Friend1 = '' 
Friend2 = ''

output_song = '' #Must be a .mid file
 
# define parallel lists to hold pitches and durations
pitches   = []
durations = []

 
# use the json file you created with parse_mbox
with open(json_file) as data:
   data=json.load(data)

monthMap = {
    "Jan":1,
    "Feb":2, 
    "Mar":3, 
    "Apr":4,
    "May":5, 
    "Jun":6, 
    "Jul":7,
    "Aug":8, 
    "Sep":9,
    "Oct":10,
    "Nov":11,
    "Dec":12
}

for email in data:
   day = int(email['Date'][5:7].replace(" ", ""))
   month = email['Date'][7:11].replace(" ", "")
   month = int(monthMap[month])
   year = int(email['Date'][11:16].replace(" ", ""))
   email['newDate'] =  datetime(year, month, day).date()

datesorted_data = sorted(data, key=lambda k: k['newDate']) #sort emails by date so we can loop through and append content

for email in datesorted_data:
   if email["From"][0:len(Friend1)+1]==Friend1: 
      wordPitches = [C2, C4, G5]#bass 
      email_content = split(email['content'])
     
   elif email["From"][0:len(Friend2)+1]==Friend2:
      wordPitches = [E2, E4, E5]#treble {allows to distinguish between friends}
      email_content= split(email['content'])

   else:
      email_content=''#don't include emails sent from others
   if len(email_content)>0:
      for keyword in keywords:
         if keyword in email['content'].lower():
            print keyword
            index = keywords.index(keyword)
            pitch = wordPitches[index]
            pitches.append(pitch)
            duration = .007*1000/len(email_content) #speed based on importance of word in conversation based on percent of total words
            durations.append(duration)

# now, pitches and durations have been created

print pitches, durations 

# so, add them to a phrase
melody = Phrase()      
melody.addNoteList(pitches, durations)

 
# view and play melody
View.notation(melody)
Play.midi(melody)
Write.midi(melody, output_song)
#midi files can be opened in GarageBand on a Mac, and from there, converted to mp3 or other desired formats
#There are also free online conversion sites, such as: http://www.zamzar.com/convert/midi-to-mp3/