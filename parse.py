from bs4 import BeautifulSoup
from urllib2 import Request, urlopen

import urllib2
from urllib2 import Request

target = 'http://www.precodoscombustiveis.com.br/postos/cidade/2568/mg/guaxupe'

content = urllib2.Request(url=target)
req = urllib2.Request(target)
response = urllib2.urlopen(req)

xhtml = response.read().decode('iso-8859-1')


soup = BeautifulSoup(xhtml)



data = []
gasolina = soup.find("span", { "class" : "lead gasolina" })
alcool = soup.find("span", { "class" : "lead alcool" })

#print (table)
#table_body2 = table.find('lead gasolina')


gasoza = gasolina.text
alcoosa = alcool.text

print (gasoza)
print (alcoosa)

#table_body = table.find('tbody')
##rows = table_body.find_all('tr')
#for row in rows:
#    cols = row.find_all('td')
#    cols = [ele.text.strip() for ele in cols]
#    data.append([ele for ele in cols if ele])
##rint (data)
