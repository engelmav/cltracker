import requests
from datastore import DataStore
from bs4 import BeautifulSoup
import re
import gmail


def perform_search(search_str,results_collector):

    base_url = 'http://sfbay.craigslist.org'

    cl_html_results = requests.get(search_str)
    soup = BeautifulSoup(cl_html_results.text, 'html.parser')

    ds = DataStore(storetype='sql')

    for result in soup.find_all(attrs={"data-pid": re.compile('\d+')}):

        link_title = result.find(id='titletextonly')

        if link_title is None:
            # print "Cannot find title for entry %s", result
            next
        else:
            datapid = result.attrs['data-pid']
            link_title_text = link_title.text

            link = '{0}{1}'.format(base_url, result.find('a').attrs['href'])

            #print "debug: {0} | {1} | {2}".format(datapid, link_title_text, link)

            ds.save_entry(datapid=datapid, title=link_title_text, url=link)

    for i in ds.new_listings:
        results_collector.append(i)

    # gm = gmail.lo('vincent.engelmann1', 'PeaceIsInternal')
    #
    # msg_content = '\n'.join(ds.new_listings)
    #
    # gm.send()

search_zips = [
    "94401",
    "94402",
    "94403",
    "94010",
    "94062",
    "94019",
    "94038"
]


car_search = 'http://sfbay.craigslist.org/search/sss?sort=rel&query=2007%20honda%20accord%20ex-l%20v+-2008'

apt_search = 'https://sfbay.craigslist.org/search/apa?search_distance=6&postal={0}&max_price=3700&bedrooms=2'


results_collector = []


for zip in search_zips:
    search_str = apt_search.format(str(zip))
    perform_search(search_str,results_collector)

if len(results_collector) > 0:
    print "found {0} new results, sending email".format(len(results_collector))
    gigantic_result_string = ''
    for i in results_collector:
        gigantic_result_string = gigantic_result_string + '\r\n' + '\r\n'.join(i) + '\r\n'

    print gigantic_result_string

    import smtplib

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login('vincent.engelmann1', 'someHashedThing')

    headers = "\r\n".join(["from: " + 'vincent.engelmann1',
                       "subject: " + 'New Entries in CL for search across {0}'.format(' '.join(search_zips)),
                       "to: " + 'vincent.engelmann1@gmail.com,moraleskd@gmail.com',
                       "mime-version: 1.0",
                       "content-type: text/plain"])

    # body_of_email can be plaintext or html!
    msg_content = gigantic_result_string
    content = headers + "\r\n\r\n" + msg_content
    session.sendmail('vincent.engelmann1', 'vincent.engelmann1@gmail.com,moraleskd@gmail.com', content.encode('ascii', 'replace'))
else:
    print "No new results"

