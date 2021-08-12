#-*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup
#olive


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'

}

data = {
    'startDate': '20180523'
}

res = requests.get('http://olive.tving.com/olive/schedule', params=data, headers=headers)
#print(res.text)

soup = BeautifulSoup(res.text, 'html.parser')

s1 = soup.find_all(attrs={'class': 'airTime'})

print(s1)
print(s1[0].string.replace(' ',''))


#print(soup.find_all(attrs={'class': 'program'}))
