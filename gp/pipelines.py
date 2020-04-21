# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv

import pandas as np
from pandas import DataFrame
class GpPipeline(object):
	#初始化
	def __init__(self):
		print("运行pipeling")
		# self.f = open("review.csv","w+",encoding='utf-8',newline="")
		# self.f1 = csv.writer(self.f)
		# column_name = ("user_name","review_content","review_time","review_rating")
		# self.f1.writerow(column_name)
	def process_item(self, item, spider):
		name_list=[]
		rating_list=[]
		time_list=[]
		content_list = []
		rating_label=[]
		content = item["reviews"]
		
		for kk in content:
			name_list.append(kk["user_name"])
			rating_list.append(kk["review_rating"])
			time_list.append(kk["review_time"])
			content_list.append(kk["review_content"])
			rating_label.append(kk["rating_label"])
		data ={"user":name_list,"rating":rating_list,"time":time_list,"rating_label":rating_label,"comment":content_list}
		df = np.DataFrame(data)
		df.to_excel('reviewFile.xls',sheet_name='Hangouts')

		# for kk in content:
		# 	data = (kk["user_name"],kk["review_rating"],kk["review_time"],kk["review_content"])
		# 	self.f1.writerow(data)
			#self.f.write("\n")
		return item
	def close_spider(self,spider):
		print("结束")
		#self.f.close()
