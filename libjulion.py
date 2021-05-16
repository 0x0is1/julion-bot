import requests, random
from bs4 import BeautifulSoup as scraper
EP_DOWNLIMIT = 50100
EP_UPLIMIT = 58885

def english_poetry_generator(soup):
    poetry = ''
    heading = soup.find(
        'h1', {'class': 'c-hdgSans c-hdgSans_2 c-mix-hdgSans_inline'})
    if heading is None: heading = scraper('N/A', 'html.parser')
    poe = soup.find('span', {'class': 'c-txt c-txt_attribution'})
    if poe is None: poe = scraper('N/A', 'html.parser')
    data = soup.find('div', {'data-view': 'PoemView'})
    if data is None: data = scraper('N/A', 'html.parser')
    lines = data.findAll(
         'div', {'style': 'text-indent: -1em; padding-left: 1em;'})
    if lines is None: lines = scraper('N/A', 'html.parser')
    header = ' '.join(heading.text.split())
    poet = ' '.join(poe.text.split())

    for line in lines:
        poetry += (' '.join(line.text.split()) + '\n')
    return header, poetry, poet


def random_url_generator(t):
    cookies = {
        '__cfduid': 'db0d58dc7534df31c08ea6f14311e80cc1606313489',
        'XSRF-TOKEN': 'eyJpdiI6IjhaU0cxNWNwSWRUaGZKdGFQd1VZMVE9PSIsInZhbHVlIjoiQzhmTnE2RzBVVlEyaEp5SjVaQVdtRHA3cTc3YUk3ejBQcE5XUGs4RGR2MGRhbzlRQ2RUMGtuS1R3UmNrUjl1VSIsIm1hYyI6IjhkYzI1YTEyM2NlYWM0MmMyYTZiMzllODg0M2Q1YzQ5MmUwMDExYTY1YzA0MzcyOWIxZjQ3MTQyNzlhZWI0MzkifQ%3D%3D',
        'laravel_session': 'eyJpdiI6IllIeTI1VW9OOW9ndnRyaW9CenpCckE9PSIsInZhbHVlIjoiTDFDK1ZlZTMxWlwvTnhDbzNUQXh2R3hvNm9CZ0lnTG5SYWJKVUV2d2V2eVQxcXc5aGI5YTRaMllDRno0MEdUMnEiLCJtYWMiOiIzOTkyMDgxZGYzNmZjZjE2YzJhZmYyNmQ1ODE3ZGE5MDRkMDQyYjNmMjEzNjlkN2UzZDk0YzViZTBiOGNjNzdkIn0%3D',
    }

    headers = {
        'Host': 'kaavyaalaya.org',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv: 75.0) Gecko/20100101 Firefox/75.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
    }
    if t==0:
        rp = random.randint(EP_DOWNLIMIT, EP_UPLIMIT)
        url = "https://www.poetryfoundation.org/poems/" + str(rp)
        return url
    if t==1:
        response = requests.head(
            'https://kaavyaalaya.org/s/random', headers=headers, cookies=cookies)
        return str(response.headers.get('location'))
        

def hindi_poetry_generator(soup):
    # This Python file uses the following encoding: utf-8
    heading = soup.find('div', {
        'style': 'margin-bottom:20px;text-align: center;font-weight: bold;text-decoration: underline;font-size: 22px;'})
    if heading is None: heading = scraper('N/A', 'html.parser')
    header = ' '.join(heading.text.split())
    poetry = soup.find('div', {
        'style': 'display: table;margin:0 auto;font-size: 20px;font-family: Mangal;max-width:98%'})
    poe = soup.find(
        'div', {'style': 'text-align: right;font-weight: bold;margin-top: 20px'})
    if poetry is None: poetry = scraper('N/A', 'html.parser')
    if poe is None: poe = scraper('N/A', 'html.parser')
    poet = ' '.join(poe.text.split())
    poetr = ''
    i = 0
    while True:
        try:
            line = poetry.findAll('br')[i].next_sibling
            if line != '          ':
                poetr += line
            i += 1
        except Exception:
            break
    if poetr is None: poetr = scraper('N/A', 'html.parser')
    return header, poetr, poet

    
'''url = random_url_generator(1)
response = requests.get(url)
soup = scraper(response.content.decode('utf-8'), 'html.parser')
a=str(hindi_poetry_generator(soup)[1]).split('\n')
print('\r' in a)
print(a)'''
