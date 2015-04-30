# final-project-dp15

THIS IS A WORK IN PROGRESS! 

This repo is meant to provide code that can be easily reused and modified to create sites similar to:
see-mail.appspot.com

Files have been commented, and some have

Where to start: 

1) Check out our website! 
http://see-mail.appspot.com. 
Give us feedback, or try our code first and give us feedback later (or do both!).

2) This project is set up for those who use Gmail for carrying out personal interactions.
Choose a relationship or set of relationships conducted over email you want to explore (suggested: at least a 1 year relationship). 
Create new labels in Gmail for that relationship (e.g. search the "To" and "from" fields, and select all, then apply labels. 
This will make your life easier in future steps, as you will have a smaller file to parse and make sense of if you apply your labels first,
rather than downloading all of your emails.

3) Download an mbox file from Google Takeout: https://www.google.com/settings/takeout
Here, you can specify the email label(s) [each label will download as a separate mbox file].

3) Open parse_mbox.py. Follow instructions to customize it to your data. Make any other modifications

4) Make some sonifications using the JEM music scripts (keyword_song.py and frequency_song.py). (Or skip this/do this later if you're not interested).
You can basically use these files as they are (just updating a few things to personalize it to your data-- instructions in the scripts).
But you can also play around with JEM (jythonmusic.org)-- there's a lot of cool things you can do that we didn't have a chance to explore.


6) Read and modify our code to create your own app on Google Appspot. 
*The "see-mail" container contains the code for the main pages, plus one of the friendship (on our site, "The Flatmate Friends")
*To access your json data from your mbox, and songs created using JEM in the app (the way we have our code currently set up), 
make sure these files are in the 'data' folder. 
*The code for the friendship using is in the folder "sougata."
*Just remember it's public, so be careful with sharing sensitive email info!
You might want to make your appspot private to you and the other person (or people) in your dataset.
We haven't tried this out, but worth considering:
http://stackoverflow.com/questions/3806016/how-to-protect-a-google-app-engine-app-with-a-password

7) Give us feedback about what the experience of analyzing your own email relationship data was like! http://tinyurl.com/kck96gr
