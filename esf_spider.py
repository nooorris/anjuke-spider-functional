import requests  
import re  
from requests.exceptions import RequestException  
from bs4 import BeautifulSoup  
from proxy_pool import get_proxys,sort_one_valid_proxy
import csv  
import time
import random
import datetime
import os


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
#获取IP代理
DUMPNAME='anjuke'+ str(datetime.date.today())

def randHeader():
    '''
    随机生成User-Agent
    :return:
    '''
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0'
                       ]
    result = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return result

def getCurrentTime():
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
 
def getURL(url, tries_num=50, sleep_time=0, time_out=10,max_retry = 50,isproxy=0):
        '''
           这里重写get函数，主要是为了实现网络中断后自动重连，同时为了兼容各种网站不同的反爬策略及，通过sleep时间和timeout动态调整来测试合适的网络连接参数；
           通过isproxy 来控制是否使用代理，以支持一些在内网办公的同学
        :param url:
        :param tries_num:  重试次数
        :param sleep_time: 休眠时间
        :param time_out: 连接超时参数
        :param max_retry: 最大重试次数，仅仅是为了递归使用
        :return: response
        '''
        sleep_time_p = sleep_time
        time_out_p = time_out
        tries_num_p = tries_num
        try:
        	res = requests.Session()
        	if isproxy == 1:
        		res = requests.get(url, headers=randHeader(), timeout=time_out, proxies=run.PROXY)
        	else:
        		res = requests.get(url, headers=randHeader(), timeout=time_out)
        	res.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            sleep_time_p = sleep_time_p + 10
            time_out_p = time_out_p + 10
            tries_num_p = tries_num_p - 1
            # 设置重试次数，最大timeout 时间和 最长休眠时间
            if tries_num_p > 0:
                time.sleep(sleep_time_p)
                print(getCurrentTime(), url, 'URL Connection Error: 第', max_retry - tries_num_p, u'次 Retry Connection')
                return getURL(url, tries_num_p, sleep_time_p, time_out_p,max_retry)
        return res


def get_one_page(url):      
	try:          
		response = requests.get(url,headers = headers)          
		if response.status_code == 200:              
			return response.text          
		return None      
	except RequestException:  
		print('error in get_one_page')          
		return None

def parse_one_page(content):   
	global DUMPNAME  
	try:          
		soup = BeautifulSoup(content,'html.parser')        
		house_list = soup.find_all('li', class_="list-item")
		if len(house_list)==0:
			print('none of house is founded in this page')
			return 1
		with open(os.path.join('./output_data',DUMPNAME+'.csv'), 'a+', encoding='UTF-8', newline='') as csvfile:
			w = csv.writer(csvfile)
			for id,house in enumerate(house_list):
				temp=[]
				Description=house.find('div',class_='house-title').a.text.strip()
				Price=house.find('span',class_='price-det').text.strip()
				Unit_price=house.find('span',class_='unit-price').text.strip()
				Link=house.find('div',class_='house-title').a['href']
				Type = house.find('div', class_='details-item').contents[1].text
				Area = house.find('div', class_='details-item').contents[3].text
				Floor = house.find('div', class_='details-item').contents[5].text
				Year = house.find('div', class_='details-item').contents[7].text
				Broker= house.find('span', class_='brokername').text.strip()[1:]      		
				Address = house.find('span', class_='comm-address').text.strip()
				Address = Address.replace('\xa0\xa0\n                  ', ' ')

				# Taglist = house.find_all('span', class_='item-tags')
				# Tag = [i.text for i in Taglist]		

				temp=[id,Area,Price,Type,Floor,Year,Unit_price,Broker,Address,Description,Link]
                
				if ~(temp == None):
					w.writerow(temp)
     
	except Exception:    
		print('error happens in try part of parse_one_page')      
		return None

