# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
import pymongo
import gp.settings as settings
from pandas import DataFrame

class GpPipeline(object):
	#初始化
	def __init__(self):
		print("运行pipeling")
		# self.f = open("review.csv","w+",encoding='utf-8',newline="")
		# self.f1 = csv.writer(self.f)
		# column_name = ("user_name","review_content","review_time","review_rating")
		# self.f1.writerow(column_name)
		'''链接数据库并保存数据'''
		
		self.client = pymongo.MongoClient("mongodb://7630:ais7630@localhost:27017/")
		self.db = self.client["7630_DB"]
		
		

	def process_item(self, item, spider):
		name_list=[]
		rating_list=[]
		time_list=[]
		content_list = []
		rating_label=[]
		content = item["reviews"]
		db_name=item["db_name"]
		self.coll =self.db[db_name]
		for kk in content:
			db_data = {"user":kk["user_name"],"rating":int(kk["review_rating"]),"time":kk["review_time"],"rating_label":int(kk["rating_label"]),"comment":kk["review_content"]}
			if self.coll.find(db_data):
				#print("********数据已经存在*****************")
				pass
			else:
				x = self.coll.insert_one(db_data)
			name_list.append(kk["user_name"])
			rating_list.append(kk["review_rating"])
			time_list.append(kk["review_time"])
			content_list.append(kk["review_content"])
			rating_label.append(kk["rating_label"])
			
		data ={"user":name_list,"rating":rating_list,"time":time_list,"rating_label":rating_label,"comment":content_list}
		df = DataFrame(data)
		df.to_excel('GoogleMeet_reviewFile.xls',sheet_name='Google_Meet')

		# for kk in content:
		# 	data = (kk["user_name"],kk["review_rating"],kk["review_time"],kk["review_content"])
		# 	self.f1.writerow(data)
			#self.f.write("\n")
		return item
	def close_spider(self,spider):
		print("结束")
		#self.f.close()
