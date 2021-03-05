import requests
import bs4

def stock(url):
    response = requests.get(url).text
    styleCode = response[response.find('styleColor" content="')+21:]
    styleCode = styleCode[:styleCode.find('"')]

    productId = response[response.find('productId" content="')+20:]
    productId = productId[:productId.find('"')]
    atk = url + '/?productId=' + productId + '&size='

    url = 'https://api.nike.com/merch/skus/v2/?filter=productId%28' + productId + '%29&filter=country%28RU%29'
    response = requests.get(url).json()['objects']
    sizes = []
    for size in response:
        sizes.append(size['nikeSize'])

    url = 'https://api.nike.com/deliver/available_gtins/v2/?filter=styleColor%28' + styleCode + '%29&filter=merchGroup%28XP%29'
    response = requests.get(url).json()['objects']
    stocks = []
    for stock in response:
        stocks.append(stock['level'])

    stockSize = {}
    for i in range(0, len(sizes)):
        stockSize[sizes[i]] = stocks[i]

    res = ''
    for key, value in stockSize.items():
        res += key + ' - ' + value + ' ' + atk + key + '\n'
    return res

if __name__ == '__main__':
    pass