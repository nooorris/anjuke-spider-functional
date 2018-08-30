import esf_spider
import analysis
import os
import csv

import requests  
import re  
import time
from requests.exceptions import RequestException  
from bs4 import BeautifulSoup 
from proxy_pool import get_proxys,sort_one_valid_proxy
import datetime


if __name__ =='__main__':
	#url='https://fz.anjuke.com/sale/cangshan/p1/#filtersort'
	#url='https://fz.anjuke.com/sale/taijiang/p1/#filtersort'
	
	PAGE=50
	FILTER_AREA=[60,150]		# 单位：平方米
	FILTER_PRICE=[0,200]		# 单位：万元	
	IS_PROXY = 0				# 是否使用代理ip,1为使用	
	DUMPNAME='CS'+ str(datetime.date.today())
	# urls=['https://fz.anjuke.com/sale/cangshan/p1/#filtersort', \
	# 		'https://fz.anjuke.com/sale/mawei/p1/#', \
	# 		'https://fz.anjuke.com/sale/taijiang/p1/#filtersort', \
	# 		]
	# urls=['https://cs.anjuke.com/sale/yuelu/p1/#filtersort','https://cs.anjuke.com/sale/kaifu/p1/#filtersort', \
	# 	'https://cs.anjuke.com/sale/furong/p1/#filtersort','https://cs.anjuke.com/sale/tianxin/p1/#filtersort']
	# urls=['https://cs.anjuke.com/sale/furong/p1/#filtersort','https://cs.anjuke.com/sale/kaifu/p1/#filtersort']
	# f=open(os.path.join('./output_data',DUMPNAME+'.csv'), 'w', encoding='UTF-8', newline='')
	# w=csv.writer(f)
	# head =['编号','面积/m²','价格/万','厅室','楼层','建造年份','单位价格','联系人','小区+详细地址','业主描述','链接']
	# w.writerow(head)
	# f.close()
    
	# for url in urls:

	# 	###########################################################################
	# 	# 1. get data from anjuke website and dump into 'result.csv' 
	# 	###########################################################################

	# 	for i in range(0,PAGE):
	# 		url=url.replace('p'+str(i),'p'+str(i+1))
	# 		if IS_PROXY==1:
	# 			proxys_list = get_proxys(1)
	# 			PROXY = sort_one_valid_proxy(proxys_list)
	# 			content=esf_spider.getURL(url,isproxy=IS_PROXY,proxy=PROXY)
	# 		content=esf_spider.getURL(url)
	# 		Flag=esf_spider.parse_one_page(content.text)
	# 		print('第{}页抓取完毕'.format(i+1))
	# 		time.sleep(2)
	# 		if Flag==1:
	# 			IS_PROXY=1




	###########################################################################
	# 2. remove duplicated ones and dump into 'result_clean.csv' 
	###########################################################################
	analysis.clean_csvdata(os.path.join('./output_data', DUMPNAME+'.csv'))

	###########################################################################
	# 3. data analysis and create html file
	###########################################################################
	analysis.filter_data(FILTER_AREA,FILTER_PRICE)
