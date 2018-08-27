import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

import json
from urllib.request import urlopen,quote
import csv
import traceback
import datetime
import os

DUMPNAME='anjuke'+ str(datetime.date.today()) 


def clean_csvdata(filepath):
	global DUMPNAME
	data=pd.read_csv(filepath)
	data.columns =['编号','面积/m²','价格/万','厅室','楼层','建造年份','单位价格','联系人','小区+详细地址','业主描述','链接']
	data=data.drop_duplicates(subset=['面积/m²','价格/万','厅室','楼层','建造年份','小区+详细地址'])
	data['编号']=[i for i in range(0,len(data))]
	data['面积/m²'] = data['面积/m²'].str.extract('(\d+)m²', expand =False)
	data['价格/万'] = data['价格/万'].str.extract('(\d+)万', expand =False)
	data['单位价格'] = data['单位价格'].str.extract('(\d+)元/m²', expand =False)
	data['建造年份'] = data['建造年份'].str.extract('(\d+)年建造', expand =False)
	data.to_csv(os.path.join('./output_data',DUMPNAME+'_clean.csv'),index=False)




def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'zeW4jk67elTZXXUbx6nylyWcub6fwbGU'
    add = quote(address)#本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url+add+'&output='+output+"&ak="+ak
    req = urlopen(url2)
    res  = req.read().decode()
    temp = json.loads(res)
    return temp



def filter_data(FILTER_AREA,FILTER_PRICE):
	global DUMPNAME
	data=pd.read_csv(os.path.join('./output_data',DUMPNAME+'_clean.csv'))
	data.columns=['id', 'area', 'price', 'room', 'floor', 'year', 'unit_price', 'contact','estate', 'description', 'link']
	fdata=data[data.area<FILTER_AREA[1]]
	fdata=fdata[fdata.area>FILTER_AREA[0]]
	fdata=fdata[fdata.price<FILTER_PRICE[1]]
	fdata=fdata[fdata.price>FILTER_PRICE[0]]
	fdata['id'] = [i for i in range(0,len(fdata))]


# df series group the imformation by estate
	df1=pd.DataFrame(fdata.estate.value_counts())
	df2=pd.pivot_table(fdata,index=['estate'],values=['year','unit_price'])

	df3=pd.merge(df1,df2,how='outer',left_index=True,right_index=True)
	df3.columns=['quantity','unit_price','year']
	df3['estate']=df3.index.get_values()
	df3['content']='{}套在售，{}年建造，均价{}元'
	df3['content']=[df3['content'][i].format(df3.quantity[i],int(df3.year[i]),int(df3.unit_price[i])) for i in range(0,len(df3))]
	df3['head']=[df3.estate[i][:df3.estate[i].find(' ')] for i in range(0,len(df3))]
	df3=df3.reset_index(drop=True)

	df4=pd.pivot_table(fdata,index=['estate','link','floor'],values='id')
	df4=pd.merge(df4,fdata,how='outer',on='id')

# dump the sorted information
	df4=df4[['estate', 'year','area', 'price', 'room', 'floor', 'unit_price', 'contact', 'description', 'link']]
	df4.columns = ['小区+详细地址','建造年份','面积/m²','价格/万','厅室','楼层','单位价格','联系人','业主描述','链接']
	writer = pd.ExcelWriter(os.path.join('./output_data',DUMPNAME+'房_已筛选_打印版.xlsx'))
	df4.to_excel(writer,'Sheet1')
	writer.save()
	print(DUMPNAME+'房_已筛选_打印版.xlsx '+'输出到文件完毕')
	df4.columns = ['estate','year','area','price','room','floor','unit_price','contact','description','link']
	df4['new_id']=[i for i in range(0,len(df4))]

# add new features to df4 for further use
	df4.drop(['contact','description'],axis=1,inplace=True)
	df4['content']= '<br/>[{6}] {0:2}m²,{1:3}万,{2},{3:8},{5}元/m²<a href=\"{4}\" style=\"color:#2f83c7\" target=\"_blank\">看房链接</a>'
	df4['content']=[df4['content'][i].format(df4.area[i],df4.price[i],df4.room[i],df4.floor[i],df4.link[i],df4.unit_price[i],df4.new_id[i]) for i in range(0,len(df4))]
	df4.index=df4.estate
	
# getting the location of estates
    

	lng=np.zeros((len(df3),1))
	lat=np.zeros((len(df3),1))
	lng=lng.tolist()
	lat=lat.tolist()
	print('printing html file... / 开始输出网页文件。。。')
	file = open(os.path.join('./output_data', DUMPNAME+'_my_buidumap.html'),'w')
	f_temp=open('template_upper.html','r')
	file.write(f_temp.read())
	f_temp.close()
	for i in range(0,len(df3)-1):

		lng[i]=(getlnglat(df3['estate'][i])['result']['location']['lng'])
		lat[i]=(getlnglat(df3['estate'][i])['result']['location']['lat'])
		df3.loc[i,'content']=df3.content[i]+''.join(df4.loc[df3.estate[i]:df3.estate[i],'content'])
		str_temp = '{content:\"'+df3.content[i].replace("\"",'\\"') +'\"' \
					+',title:\"'+df3['head'][i]+'\"' \
					+',imageOffset: {width:0,height:3}' \
					+',position:{lat:'+str(lat[i])+',lng:'+str(lng[i])+'}},\n'
		file.write(str_temp)
	i = len(df3)-1
	lng[i]=(getlnglat(df3['estate'][i])['result']['location']['lng'])
	lat[i]=(getlnglat(df3['estate'][i])['result']['location']['lat'])
	df3.loc[i,'content']=df3.content[i]+''.join(df4.loc[df3.estate[i]:df3.estate[i],'content'])
	str_temp = '{content:\"'+df3.content[i].replace("\"",'\\"') +'\"' \
				+',title:\"'+df3['estate'][i]+'\"' \
				+',imageOffset: {width:0,height:3}' \
				+',position:{lat:'+str(lat[i])+',lng:'+str(lng[i])+'}}\n'
	file.write(str_temp)

	# try:
	# 	lng[len(df3)]=(getlnglat(df3['estate'][len(df3)])['result']['location']['lng'])
	# 	lat[len(df3)]=(getlnglat(df3['estate'][len(df3)])['result']['location']['lat'])
	# 	df3.loc[len(df3),'content']=df3.content[len(df3)]+''.join(df4.loc[df3.estate[len(df3)]:df3.estate[len(df3)],'content'])
	# 	str_temp = '{content:\"'+df3.content[len(df3)].replace("\"",'\\"') +'\"' \
	# 				+',title:\"'+df3['estate'][len(df3)]+'\"' \
	# 				+',imageOffset: {width:0,height:3}' \
	# 				+',position:{lat:'+str(lat[len(df3)])+',lng:'+str(lng[len(df3)])+'}}\n'
	# 	file.write(str_temp)
	# except:
	# 	f = open(os.path.join('./output_data',"异常日志.txt"),'a')
	# 	traceback.print_exc(file=f)
	# 	f.flush()
	# 	f.close()

	f_temp=open('template_lower.html','r')
	file.write(f_temp.read())
	f_temp.close()
	file.close()
	print('printing html file done / 网页文件生成完毕')


