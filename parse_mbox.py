#for parsing mbox file into a json
#will want another script for parsing the json
import mailbox
import email
import json
#import chardet
#import html2text
from BeautifulSoup import BeautifulStoneSoup
#from HTMLParser import HTMLParser

MBOX = '/Users/akasunic/Desktop/DataPipeline/Final Project/Takeout 2/Mail/Kendall.mbox'

# A routine that makes a ton of simplifying assumptions
# about converting an mbox message into a Python object

def html_convert(text):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    

    #postContent = html2text.html2text(text).encode('ascii', 'ignore')
    sections = text.partition("> wrote:")
    sections = sections[0].partition(">wrote:")
    sections2 = sections[0].rpartition("On ")
    words = [x for x in sections2 if x != '']
    #words = sections2[0].split() 
    #parser = HTMLParser()
    #html_decoded_string = parser.unescape(postContent)
    text = " ".join([word for word in words if word.isalpha()])
    #return sections2
    
    try:
        replaced=words[0].replace("\r", ' ')
        replaced2 = replaced.replace("\n", ' ')
    except IndexError:
        return ''
    text = unicode(BeautifulStoneSoup(replaced2, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    return text
    
def get_text(msg):
    text = ""
    if msg.is_multipart():
        html = None
        '''for part in msg.get_payload():
            if part.get_content_charset() is None:
                #charset = part.detect(str(part))['encoding']
                pass
            else:
                charset = part.get_content_charset()
            if part.get_content_type() == 'text/plain'
                text = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
            if part.get_content_type()[0:9] == 'text/html':
                html = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')'''
        part = msg.get_payload()   

        if part[0].get_content_charset() is None:
            #charset = part[0].detect(str(part))['encoding']
            return ""
            #pass
            
        else:
            charset = part[0].get_content_charset()
        if part[0].get_content_type() == 'text/plain':
            text = unicode(part[0].get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
        else:
            print part[0].get_content_type()
        if part[0].get_content_type() == 'text/html':
            print 'FOUND HTML'
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
    

def objectify_message(msg):
    
    
    keys = ['Date', 'Subject', 'From', 'To', 'content', 'Content-Type', 'Received']
    # Map in fields from the message
    o_msg = dict([ (k, v) for k, v in msg.items() ])
    
    # Assume one part to the message and get its content
    # and its content type
    
    #part = [p for p in msg.walk()][0]
    #o_msg['contentType'] = part.get_content_type()

    text= html_convert(get_text(msg))
    text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    
    #text = BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    o_msg['content'] = text
    #lots of long html contents, but they were all from PopMoney so I got rid of them!
    #otherwise these would be flagged as long (and thereby potentially important) emails
    #assuming this will be the case for most data
    if o_msg['content'][0:4]=="<html>":
        o_msg['content'] = o_msg['Subject']
    n_msg ={}
    for k in o_msg:
        if k in keys:
            n_msg[k] = o_msg[k]
    
    
    return n_msg
    
# Create an mbox that can be iterated over and transform each of its
# messages to a convenient JSON representation

mbox = mailbox.UnixMailbox(open(MBOX, 'rb'), email.message_from_file)

messages = []

while 1:
    msg = mbox.next()

    if msg is None: break
    
        
    messages.append(objectify_message(msg))
print messages [0:1] 
    
with open('data.json', 'w') as outfile:
    json.dump(messages, outfile, indent=1)
