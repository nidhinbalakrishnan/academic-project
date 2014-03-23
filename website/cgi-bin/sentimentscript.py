#!/usr/bin/python

#Import modules for CGI handling
import cgi, cgitb
import math
import review_test
import os

#Create instance of field storage
form=cgi.FieldStorage()

#Get data form fields
reviewtext=form.getvalue('reviewtext')
#reviewtext = 'I like this movie.'

positiveResult='<h3 style="color:green">The Review is Positive</h3>'
negativeResult='<h3 style="color:red">The Review is Negative</h3>'

def test_review(textinput):
        #fullname = os.path.join(path,'samplereview.txt')
	filid = open('samplereview.txt','w')
        filid.write(textinput)
        filid.close()
	value = review_test.review_test(1)
	fid = open('output.txt','w')
	fid.write(str(value))
        fid.close()
	return value

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Proximity based Sentiment Analysis - Home</title>"

print "</head>"
print '<body style="margin-top:10px">'
print '<div id="container" align="center">'
print '<div align="left" style="margin-left:250px">'
print "<br><h3><u>The review is</u> :<br></h3><h5> %s</h5><br>" % (reviewtext)

value=test_review(reviewtext)
#value = 1


print '<br><h3><u>Result of Analysis</u> :<br></h3>'
if value:
	print '%s' % positiveResult
else:
	print '%s' % negativeResult
print '</div>'
print '<br><br><center><a href="http://localhost/index.html"><button>Try another review</button></a></center>' 
print '</div>'
print "</body>"
print "</html>"

