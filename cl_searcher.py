import requests
from datastore import DataStore
from bs4 import BeautifulSoup
import re

SEARCH_LINK = """
http://sfbay.craigslist.org/search/sss?sort=rel&query=2007%20honda%20accord%20ex-l%20v+-2008&searchNearby=1
"""

cl_html_results = requests.get('http://sfbay.craigslist.org/search/sss?sort=rel&query=2007%20honda%20accord%20ex-l%20v+-2008')
soup = BeautifulSoup(cl_html_results.text, 'html.parser')

ds = DataStore(storetype='sql')

for result in soup.find_all(attrs={"data-pid": re.compile('\d+')}):

    link_title = result.find(id='titletextonly')

    if link_title is None:
        # print "Cannot find title for entry %s", result
        next
    else:
        print result.attrs['data-pid'], link_title.text

    #print result.attrs['data-pid'], link_title

    # price = result.find(class_='price')
    # if price is None:
    #     next
    # else:
    #     print price.text
