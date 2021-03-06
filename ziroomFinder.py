import requests
from bs4 import BeautifulSoup
import re

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, sdch',
           'Accept-Language':'zh-CN,zh;q=0.8',
           'Cache-Control':'max-age=0',
           'Cookie':'CURRENT_CITY_CODE=110000; PHPSESSID=b4bj1qprsc78qqtidpnauvouc7; CURRENT_CITY_NAME=%E5%8C%97%E4%BA%AC; BJ_nlist=%7B%22244406%22%3A%7B%22id%22%3A%22244406%22%2C%22sell_price%22%3A1830%2C%22title%22%3A%22%5Cu77f3%5Cu666f%5Cu5c71%5Cu9c81%5Cu8c371%5Cu53f7%5Cu7ebf%5Cu516b%5Cu89d2%5Cu6e38%5Cu4e50%5Cu56ed%5Cu516d%5Cu5408%5Cu56ed3%5Cu5c45%5Cu5ba4-%5Cu5317%5Cu5367%22%2C%22add_time%22%3A1497675479%2C%22usage_area%22%3A9%2C%22floor%22%3A%224%22%2C%22floor_total%22%3A%2222%22%2C%22room_photo%22%3A%22g2%5C%2FM00%5C%2F23%5C%2F8E%5C%2FChAFD1lCKAKAAnXOAAWmC75LXFQ344.jpg%22%2C%22city_name%22%3A%22%5Cu5317%5Cu4eac%22%7D%7D',
           'Host':'www.ziroom.com',
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def getMetaDataFromZiroom(site_url):
    print(site_url)
    response = requests.get(site_url, headers=headers)
    response.raise_for_status()  # Something failed?
    soup = BeautifulSoup(response.content, 'html.parser')

    # no page ?
    noPage = soup.find('div', class_='nopage')
    if noPage:
        return False, False

    try:
        # internalLinks
        internalLinkTags = soup.findAll(href=re.compile('/z/vr/[0-9]+\.html'))
        internalLinks = set()
        for internalLinkTag in internalLinkTags:
            internalLinks.add('http://www.ziroom.com'+internalLinkTag['href'])
        
        # upsale ?
        room_status = soup.find('a', id='zreserve')
        if not room_status:
            room_status = False
        else:
            room_status = True

        # name
        room_name = soup.find('div', class_='room_name').h2.get_text().strip()

        # price
        pricePattern = re.compile(r'[-+]?[0-9]*\.?[0-9]+')
        room_price = pricePattern.search(soup.find('span', class_='room_price').get_text()).group()

        # house area and direction
        room_detail = soup.find('ul', class_='detail_room').contents
        areaPattern = re.compile(r'[-+]?[0-9]*\.?[0-9]+')
        room_area = areaPattern.search((room_detail[1]).get_text()).group()
        directionPattern = re.compile(r'[东南西北]')
        room_direction = directionPattern.search((room_detail[5]).get_text()).group()
    
        room_location_tag = soup.find(attrs={'data-lng':True})
        room_location = [room_location_tag['data-lng'], room_location_tag['data-lat']]

    except:
        if internalLinks:
            return False, internalLinks
        else:
            return False, False
    
    return {'room_name':room_name,
            'room_price':room_price,
            'room_area':room_area,
            'room_direction':room_direction,
            'room_location':room_location,
            'room_status':room_status
    }, internalLinks
        



