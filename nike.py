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
            stockSize[sizes[i]] = stocks[i]

        res = ''
        for key, value in stockSize.items():
            res += key + ' - ' + value + '\n'
        res += atk + '9'
        return res
    
    #parse new items
    while True:
        try:
            response = requests.get('https://www.nike.com/ru/launch?s=upcoming', headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}).text
            soup = BeautifulSoup(response, 'html.parser')
            products = soup.find_all('figure', {'class': 'pb2-sm va-sm-t ncss-col-sm-12 ncss-col-md-6 ncss-col-lg-4 pb4-md prl0-sm prl2-md ncss-col-sm-6 ncss-col-lg-3 pb4-md prl2-md pl1-md pr0-md d-sm-h d-md-ib'})
            for product in products:
                if product.get_text() in all_items: continue
                ptext = product.find('h3', {'class': 'headline-5'}).get_text()
                ptext += product.find('h6', {'class': 'headline-3'}).get_text()
                ptext = ptext.replace('\n', ' ')
                ptext += '\n' + product.find('p', {'class': 'headline-4'}).get_text() + ' ' + product.find('p', {'class': 'headline-1'}).get_text() + '\n'
                ptext += stock('https://www.nike.com' + product.find('a', {'class': 'card-link d-sm-b'})['href'])
                discord_webhook.DiscordWebhook(url=wb,
                                            content=ptext[:2000]).execute()
                all_items.append(product.get_text())
                time.sleep(5)
            time.sleep(5)
        except: print(traceback.format_exc())

if __name__ == '__main__':
    nike()
