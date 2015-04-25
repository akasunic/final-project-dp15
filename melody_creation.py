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


# define vowels, will later match with corresponding musical pitches
# i.e., first vowel goes with first pitch, and so on.
vowels       = "aeiou"
 
# define consonants
consonants = "bcdfghjklmnpqrstvwxyz"
 
# define parallel lists to hold pitches and durations
pitches   = []
durations = []
 
# factor used to scale durations 
durationFactor = 0.1   # higher for longer durations
 
# use the json file you created with parse_mbox
with open("/Users/akasunic/Desktop/DataPipeline/Final Project/final-project-practice/data/data.json") as data:
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

date_prev = data[0]["newDate"] + timedelta(days=-1) #set a starting point that is one day before the first email sent

for email in datesorted_data:
   if email["From"][0:4]=="Kend": 
      vowelPitches = [C3, D3, E3, G3, A3]#bass 
      email_content = split(email['content'])
      gap = email["newDate"]-date_prev
      date_prev = email["newDate"]
   elif email["From"][0:4]=="Anna":
      vowelPitches = [C4, D4, E4, G4, A4]#treble {allows to distinguish between friends
      email_content= split(email['content'])
      gap = email["newDate"]-date_prev
      date_prev = email["newDate"]
   else:
      email_content=''#don't include emails sent from others
   if len(email_content)>0:
      for word in email:
         for char in word:
            if char in vowels:
               index = find(vowels, char)
               pitch = vowelPitches[index]
               pitches.append(pitch)
               duration = gap.days*durationFactor/len(email_content) #speed of melody based on both how quickly respond and how much is said
               if duration <=0:
                  duration = 0.001
               durations.append(duration)

# now, pitches and durations have been created

print pitches, durations 

# so, add them to a phrase
melody = Phrase()      
melody.addNoteList(pitches, durations)

 
# view and play melody
View.notation(melody)
Play.midi(melody)
Write.midi(melody, "AnnaKendallFreq.mid")
#midi files can be opened in GarageBand on a Mac, and from there, converted to mp3 or other desired formats
#There are also free online conversion sites, such as: http://www.zamzar.com/convert/midi-to-mp3/
