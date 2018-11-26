#   This script is an example of how to use regular expression in web scraping.
#   What this script does not really demonstrate is how to parse the data.
#   I would suggest putting that in a for loop or using LXML library to identify tags
#   webaddress = r'http://www.latlong.net/category/cities-236-15.html'

import urllib
import re


webaddress = r'http://www.latlong.net/category/cities-236-15.html'
webPage = urllib.urlopen(webaddress)

#   What did urllib fetch?
#   type(webPage), dir(webPage)
#   data = webPage.read()
#   webPage.close()

#   This is a snippet that we will use for matching regular expressions on
fullline = r"""<a href="/place/elgin-il-usa-9870.html" title="Elgin, IL, USA" >Elgin, IL, USA</a></td><td>42.035408</td><td>-88.282570</td>\n</tr>\n<tr>\n<td>"""
start = fullline.find('>')
stop = fullline.find('</a>')
line = fullline[start:stop]
#Oneliner line = fullline[fulline.fine('>'):fullline.find('</a>')]


city_pattern = r'(>)([a-zA-Z]*,)(\s[A-Z]*,)(\s[A-Z]*)'
matches = re.match(city_pattern, line)
print matches.group()

city_pattern2 = r'(>)([a-zA-Z]*)(,)(\s[A-Z]*)(,)(\s[A-Z]*)'
matches = re.match(city_pattern2, line)
print matches.group()

##Here is some code that matches the coordinates
line = fullline[fullline.find('<td>'):]
coord_pattern = r'(<td>)([0-9]*.[0-9]*)(</td>)(<td>)([0-9]*|\-[0-9]*.[0-9]*)(</td>)'
matches = re.match(coord_pattern, line)
print matches.group()

#Another example of how to match things
table_entry = r"""<td><a href="http://www.latlong.net/place/muskegon-mi-usa-21625.html" title="Muskegon, MI, USA" >Muskegon, MI, USA</a></td><td>43.224194</td><td>-86.235809</td>"""
# pattern = r'(<td><a href="http://www.latlong.net/place/)([a-zA-Z]*)- '
# pattern = r'(<td><a href="http://www.latlong.net/place/)([a-zA-Z]*)(-)([a-zA-Z]*)'
# pattern = r'(<td><a href="http://www.latlong.net/place/)([a-zA-Z]*)(-)([a-zA-Z]*)(-)([a-zA-Z]*)(*)(<td>)'



