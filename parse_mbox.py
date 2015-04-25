#for parsing mbox file into a json
#mbox files can be downloaded using Google Takeout:
#https://www.google.com/settings/takeout
#We highly recommend searching within Gmail and creating labels for the friendship you want to explore
#You can then 'takeout' only the emails that fall under that label

import mailbox
import email
import json
from BeautifulSoup import BeautifulStoneSoup

#To reuse this code, change the file path below to point to your mbox file
MBOX = '/Users/akasunic/Desktop/DataPipeline/Final Project/Takeout 2/Mail/Kendall.mbox'

#email content text is super messy! this function uses some rules to clean it up.
#only keep the most recent thread to avoid duplication of emails
#most email say, "On [date] [person] wrote:", so here we partition by wrote
#and keep just the first part
def html_convert(text):
    
    if "wrote:" in text:
        text = text.partition("wrote:")[0]
    
    #replace common html items to make the message clearer to read
    try:
        replaced=text.replace("\r", ' ')
        replaced2 = replaced.replace("\n", ' ')
    except IndexError:
        replaced2 = text
    #apply BeautifulStoneSoup to make any additional changes (though I think this doesn't do much)
    text = unicode(BeautifulStoneSoup(replaced2, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    return text

#email content in mbox files can be stored in multiparts
#this function uses some simplifying assumptions
#to get the main content   
def get_text(msg):
    text = ""
    if msg.is_multipart():
        html = None
        
        part = msg.get_payload()   

        if part[0].get_content_charset() is None:
            return ""
            
        else:
            charset = part[0].get_content_charset()
        if part[0].get_content_type() == 'text/plain':
            text = unicode(part[0].get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
        #else:
            #print part[0].get_content_type() #this was used for testing code, may be useful
        if part[0].get_content_type() == 'text/html':
            #print 'FOUND HTML' #this was used for testing code, may be useful
            html = unicode(part[0].get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
        
        if html is None:
            return text.strip()
        else:
            return html.strip()
    else:
        try:
            text = unicode(msg.get_payload(decode=True),msg.get_content_charset(),'ignore').encode('utf8','replace')
            return text.strip()
        except:
            return ""
    

#creates a dictionary for each email message in the mbox file
#the argument for this function (msg) refers to 1 email message
def objectify_message(msg):
    
    #this list of keys may be modified depending on one's data exploration preferences
    #for example, we left in "Received" even though we did not use it in all charts
    #the Received field allows you to get IP address
    #other fields may also be of interest
    keys = ['Date', 'Subject', 'From', 'To', 'content', 'Content-Type', 'Received']
    
    # Map in fields from the message
    o_msg = dict([ (k, v) for k, v in msg.items() ])
    
    #get and clean up the text from the email
    text= html_convert(get_text(msg))
    
    #set content key equal to the cleaned up text 
    o_msg['content'] = text
    
    #------Do some additional cleaning----------
    #Users may want to modify this section to fit their own data and exploration preferences
    
    #not all html messages were accurately read as Content-type html
    #there were several long text emails containing html elements (e.g. PopMoney from PNC) that were screwing with the data analysis
    #so here, we edit that so that we don't give undue importance
    #to emails that are actually just saying 'I sent you rent money'
    #a similar rationale is used below for craiglist and forwarded emails
    if o_msg['content'][0:6]=="<html>":
        o_msg['content'] = o_msg['Subject']
    if "CRAIGSLIST ADVISORY" in o_msg['content']:
        o_msg['content'] = "Craigslist communications" #avoids giving undue importance to long Craiglist emails
    try:
        if o_msg['Subject'][0:3]=="Fwd":
            o_msg['content'] = o_msg['Subject']#avoids giving undue importance to long forwarded emails
    #below, catches exception if subject line is less than 3 characters:
    except KeyError:
        pass 
    
    #o_msg contains additional keys besides the ones in our keys list
    #so we create a new dictionary for only those keys that we deem relevant
    n_msg ={}
    for k in o_msg:
        if k in keys:
            n_msg[k] = o_msg[k]
    return n_msg
    

#Uses the mailbox library to create an mbox that can be iterated over and transform each of its
# messages to a convenient JSON representation
#see online for documentation
mbox = mailbox.UnixMailbox(open(MBOX, 'rb'), email.message_from_file)

messages = []

while 1:
    msg = mbox.next()
    if msg is None: break
    messages.append(objectify_message(msg))

#To reuse this code, change output location    
with open('/Users/akasunic/Desktop/DataPipeline/Final Project/final-project-practice/data/data.json', 'w') as outfile:
    json.dump(messages, outfile, indent=1)
