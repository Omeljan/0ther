import requests
from bs4 import BeautifulSoup


URL = 'https://auto.ria.com/newauto/marka-jeep/'
#Windows
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
			 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
'''
Linux
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0', 
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
'''
FILE = 'cars.csv'

def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	return r

def get_pages_count(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('span', class_='mhide')
	if pagination:
		return int(pagination[-1].get_text())
	else:
		return 1

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='proposition')

	cars =[]
	for item in items:
		uan_price = item.find('span', class_='grey size13')
		if uan_price:
			uan_price = uan_price.get_text()
		else:
			uan_price = "Цену уточняйте"
		cars.append({

			'title': item.find('div', class_='proposition_title').get_text(strip=True),
			'link': HOST + item.find('a').get('href'),
			'usd_price': item.find('span', class_='green').get_text(strip=True),
			'uan_price': uan_price,
			'region': item.find('svg', class_='svg-i16_pin').find_next('strong').get_text(),
			})
	return cars

def save_file(items, path):
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Марка','Ссылка','Цена в $','Цена в UAN','Город'])
		for item in items:
			writer.writerow([item['title'],item['link'],item['usd_price'],
				             item['uan_price'],item['region']])


def parse():
	html = get_html(URL)
	if html.status_code == 200:
		cars = []
		pages_count = get_pages_count(html.text)
		for page in range(1, pages_count + 1):
			print(f'Парсинг страницы {page} из {pages_count} ... ')
			html = get_html(URL, params={'page': page})
			cars.extend(get_content(html.text))
		save_file(cars, FILE)
		print(f'Получено {len(cars)} автомобилей')
		#cars = get_content(html.text)
	else:
		print('Error')


parse()
