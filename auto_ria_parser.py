import requests
from bs4 import BeautifulSoup


URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
			 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://auto.ria.com'

def get_html(url, params=None):
	r= requests.get(url, headers=HEADERS, params=params)
	return r

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='proposition')

	cars = []
	for item in items:
		uan_price= item.find('span', class_='grey size13')
		if uan_price:
			uan_price = uan_price.get_text(strip=True)
		else:
			uan_price = 'Цену уточняйте'
		cars.append({
			'title': item.find('h3', class_='proposition_name').get_text(strip=True),
			'link': HOST + item.find('a', class_= None).get('href'),
			'usd_price': item.find('span', class_='green').get_text(strip=True),
			'uah_price': uan_price, 
			'city': item.find('svg', class_='svg svg-i16_pin').find_next('strong').get_text(strip=True),
			})
	for car in cars:
		print(car)

def parse():
	html =get_html(URL)
	if html.status_code == 200:
		get_content(html.text)
	else:
		print("Error")




parse()