# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import traceback
import discord_webhook
import time
import json
import os
import threading

filePath = os.path.dirname(os.path.abspath(__file__))

all_info = {"all_items": ["19 Mar Air Max 95 x Kim JonesДоступно 3/19 в 11:00 AM"], "adidas_result": ""}
#try:
#    config_path = filePath + '\\config.json'
#    with open(config_path, encoding='utf-8') as f:
#        all_info = json.loads(f.read())
#except: pass
wb = 'https://discord.com/api/webhooks/817344618080501760/m3TA7dndamTgHYAL2YpW42izfAOhxMTrzmqrDvB9QSZg6mQiXC6T7cCkAdQXltQroXHu'

def nike():
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
            for product in products:
                if product.get_text() in all_info['all_items']: continue
                ptext = product.find('a', {'class': 'card-link d-sm-b'})['href']
                ptext = ptext[13:]
                ptext = ptext.replace('\n', ' ')
                ptext += '\n' + product.find('div', {'class': 'available-date-component'}).get_text() + '\n'
                ptext += stock('https://www.nike.com' + product.find('a', {'class': 'card-link d-sm-b'})['href'])
                discord_webhook.DiscordWebhook(url=wb, content=ptext).execute()
                all_info['all_items'].append(product.get_text())
                #with open(config_path, "w", encoding='utf-8') as f:
                #    json.dump(all_info, f, ensure_ascii=False)
        except: print(traceback.format_exc())
        time.sleep(5)

def adidas():
    url = 'https://www.adidas.ru/yeezy'
    while True:
        try:
            response = requests.get(url, headers={
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}, proxies={'https' : "https://MiSyCcnd:qVgHXfYS@45.138.147.177:53094"}).text
            response = response[response.find('window.ENV = ')+12:]
            response = response[:response.find('</script>')]
            info = json.loads(response)
            result = ''
            for product in info['productIds']:
                result += 'ProductID: ' + product + '\n'
                result += 'Name: ' + info['productData'][product]['localized']['productName'] + ' ' + info['productData'][product]['localized']['color'] + '\n'
                result += 'Price: ' + info['productData'][product]['localized']['priceFormatted'] + '\n'
                result += 'ReleaseDate: ' + info['productData'][product]['localized']['releaseDate'].encode('latin1').decode('utf8') + '\n\n'
            
            if result == '': result += 'No products now\n\n'

            result += 'Больше информации на https://www.adidas.ru/yeezy'
            if result != all_info['adidas_result']: 
                discord_webhook.DiscordWebhook(url='https://discord.com/api/webhooks/821033169721360454/k53TcQxWpZXzYC3aR8O5H_chWcn2mVrw2d2ANNgHcUYvOQjpDD-2zqiFT9_LFs7MXKCO', content=result).execute()
                all_info['adidas_result'] = result
                #with open(config_path, "w", encoding='utf-8') as f:
                #    json.dump(all_info, f, ensure_ascii=False)
        except: print(traceback.format_exc())
        time.sleep(5)

if __name__ == '__main__':
    threads = []

    threads.append(threading.Thread(target=nike))
    threads[-1].start()
    
    threads.append(threading.Thread(target=adidas))
    threads[-1].start()

#pyarmor pack -e " --onefile" --name "snkrsParser" --clean snkrs.py
