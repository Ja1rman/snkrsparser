import requests
from bs4 import BeautifulSoup
import traceback
import discord_webhook
import time

wb = 'https://discord.com/api/webhooks/817344618080501760/m3TA7dndamTgHYAL2YpW42izfAOhxMTrzmqrDvB9QSZg6mQiXC6T7cCkAdQXltQroXHu'

def nike():
    all_items = []

    #check stock and atk
    def stock(url):
        response = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}).text
        styleCode = response[response.find('styleColor" content="')+21:]
        styleCode = styleCode[:styleCode.find('"')]

        productId = response[response.find('productId" content="')+20:]
        productId = productId[:productId.find('"')]
        atk = url + '/?productId=' + productId + '&size='

        url = 'https://api.nike.com/merch/skus/v2/?filter=productId%28' + productId + '%29&filter=country%28RU%29'
        response = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}).json()['objects']
        sizes = []
        for size in response:
            sizes.append(size['nikeSize'])

        url = 'https://api.nike.com/deliver/available_gtins/v2/?filter=styleColor%28' + styleCode + '%29&filter=merchGroup%28XP%29'
        response = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}).json()['objects']
        stocks = []
        for stock in response:
            stocks.append(stock['level'])

        stockSize = {}
        for i in range(0, len(sizes)):
            try:stockSize[sizes[i]] = stocks[i]
            except: pass

        res = ''
        k = ''
        for key, value in stockSize.items():
            res += key + ' - ' + value + '\n'
            k = key
        res += atk + k
        return res
    
    #parse new items
    while True:
        try:
            response = requests.get('https://www.nike.com/ru/launch?s=upcoming', headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}).text
            soup = BeautifulSoup(response, 'html.parser')
            products = soup.find_all('figure', {'class': 'd-md-h ncss-col-sm-12 va-sm-t pb0-sm prl0-sm'})
            for product in products[4:]:
                if product.get_text() in all_items: continue
                ptext = product.find('a', {'class': 'card-link d-sm-b'})['href']
                ptext = ptext[13:]
                ptext = ptext.replace('\n', ' ')
                ptext += '\n' + product.find('div', {'class': 'available-date-component'}).get_text() + '\n'
                ptext += stock('https://www.nike.com' + product.find('a', {'class': 'card-link d-sm-b'})['href'])
                discord_webhook.DiscordWebhook(url=wb,
                                            content=ptext).execute()
                all_items.append(product.get_text())
                time.sleep(1)
        except: print(traceback.format_exc())

if __name__ == '__main__':
    nike()
