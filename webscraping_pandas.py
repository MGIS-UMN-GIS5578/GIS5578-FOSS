###https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
from bs4 import BeautifulSoup
import requests
import pandas as pd

theUrl = r'http://www.latlong.net/category/cities-236-15.html'
webpage = requests.get(theUrl)
parsedWebPage = BeautifulSoup(webpage.content)

parsedWebPage.title

#This will find ALL of the tables, you can narrow it down with the class tag
allTables = parsedWebPage.find_all('table')

dataTable = parsedWebPage.find('table')
#Skip the header row in the table
#print(dataTable.next())

#Dictionary that will hold all of the information
dataDictionary = {}
for rec, row in enumerate(dataTable):
    print row
    try:
        
        #Split it into parts row.findAll('td')[0].text.split(',')
    
        city, state, country = row.findAll('td')[0].text.split(',')
    
        latitude = row.findAll('td')[1].text
        longitude = row.findAll('td')[2].text

        dataDictionary[str(rec)] = {'city': city, 'state': state, 'country': country, 'latitude': latitude, 'longitude': longitude}
    except IndexError as e:
        pass
        #incase something wierd happens ignore it/handle it
    except ValueError as e:
        pass
        #If a place name doesn't have city state, country

df = pd.DataFrame.from_dict(dataDictionary, orient='index')

print(df)