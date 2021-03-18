# -*- coding: utf-8 -*-

import telebot
import requests
import traceback
import multiprocessing as mp
import time
import random
from bs4 import BeautifulSoup
import discord_webhook
import re

def dns():
    url = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?q=radeon%20rx%206700%20xt'
    
    while True:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"})
            soup = BeautifulSoup(response.text, 'html.parser')
            soup = soup.find_all('a', {'class': 'catalog-product__name ui-link ui-link_black'})
            for href in soup:
                try:
                    link = 'https://www.dns-shop.ru' + href['href']
                    response = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"})
                    price = response.text
                    price = price[price.find('price":')+7:]
                    price = price[:price.find(',')]
                    price = int(price)
                    if price > 35000 and price < 60000:
                        s = BeautifulSoup(response.text, 'html.parser')
                        s = s.find('h1', {'class': 'page-title product-card-top__title'})
                        if '6700' in s.get_text():
                            discord_webhook.DiscordWebhook(url='https://discord.com/api/webhooks/822164863404867654/He8zzdoOsbwWYwXcsfiMpuRPQyTF2Zug0FaYlOp2JBMUDn50ZaPsNNCLKdToIriTmGa4', content=link).execute()
                except: print(traceback.format_exc())
        except: print(traceback.format_exc())

dns_href = ['https://www.dns-shop.ru/product/9483d2a485eed760/videokarta-pci-e-asrock-amd-radeon-rx-6700-xt-challenger-pro-12288mb-192bit-gddr6-rx6700xt-clp-12go-hdmi-dp/',
            'https://www.dns-shop.ru/product/75190cb578033332/videokarta-msi-amd-radeon-rx-6700-xt-mech-2x-rx-6700-xt-mech-2x-12g-oc/']

def dns_with_href():
    while True:
        for link in dns_href:
            try:
                response = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"})
                price = response.text
                price = price[price.find('price":')+7:]
                price = price[:price.find(',')]
                price = int(price)
                if price > 35000 and price < 60000:
                    s = BeautifulSoup(response.text, 'html.parser')
                    s = s.find('h1', {'class': 'page-title product-card-top__title'})
                    if '6700' in s.get_text():
                        discord_webhook.DiscordWebhook(url='https://discord.com/api/webhooks/822164863404867654/He8zzdoOsbwWYwXcsfiMpuRPQyTF2Zug0FaYlOp2JBMUDn50ZaPsNNCLKdToIriTmGa4', content=link).execute()
            except: pass

if __name__ == "__main__":
    threads = []

    threads.append(mp.Process(target=dns))
    threads[-1].start()

    threads.append(mp.Process(target=dns_with_href))
    threads[-1].start()
