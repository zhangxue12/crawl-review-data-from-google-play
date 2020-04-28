import scrapy
from gp.items import gpItem
import re
class GooglePlayCrawl(scrapy.Spider):
	"""docstring for GooglePlayCrawl"""
	name = 'gp'
	allowed_domains = ["play.google.com"]
	def __init__(self,*args,**kwargs):
		
		urls = kwargs.pop('urls',[]) #获取参数
		if urls:
			self.start_urls = urls.split(",")
		print("start urls =", self.start_urls)
		
		#self.start_urls = ["https://play.google.com/store/apps/details?id=us.zoom.videomeetings&showAllReviews=true&hl=en"]
	def parse(self,response):
		print('Begin crawl',response.url)
		url_check=response.url
		url_check=url_check.split(".")
		#确定当前爬取的时哪一个app
		for item in url_check:
			if "zoom" == item:
				db_name="Zoom"
				break
			elif "alibaba" == item:
				db_name="Ding_Talk"
				break
			elif "apps" == item:
				db_name="Google_Meet"
				break
		content = response.xpath("//div[@class='LXrl4c']")
		exception_count = 0
		item = gpItem()
		try:
			review = response.xpath('//div[@jscontroller="H6eOGe"]')
			print(len(review))
			
			content_list = []

			for i in review:
				dic = {}
				user_name = i.xpath('div/div[2]/div[1]/div[1]/span/text()')[0].extract().strip()
				rating = i.xpath('div/div[2]/div[1]/div[1]/div/span[1]/div/div/@aria-label')[0].extract()
				re_time =i.xpath('div/div[2]/div[1]/div[1]/div/span[2]/text()')[0].extract().strip()
				rating_star = re.search(r"\d+", rating).group(0)
				review_text = i.xpath('div/div[2]/div[2]/span/text()').extract()
				#print(type(re_time))
				#print(review_text)
				#print("==========================================")
				# time preprocess
				if int(rating_star)==4:
					rating_label = "0"
				elif int(rating_star)==5:
					rating_label = "1"
				else:
					rating_label ="-1"

				month=["January","February","March","April","May","June","July","August","September","October","November","December"]
				re_time = re_time.split(" ")
				print(re_time)
				if re_time[0] in month:
					month_t = month.index(re_time[0])+1
					print(month_t)
				review_time = str(re_time[2])+"/"+str(month_t)+"/"+str(re_time[1])
				review_time = review_time[:-1]
				print(review_time)
				#print(type(review_time ),review_time)
				# filter reviews with Chinese or other language or expression
				flag = 0
				review_p = review_text[0].split(" ")
				
				for word in review_p:
					if all(ord(c)<122 for c in word)==True:
						flag =0
					else :
						flag += 1
				#print(review_text,flag)
				if flag == 0:
					review_text = " ".join(list(review_text)).strip()
					dic['user_name']=user_name
					#print(rating_star)
					dic['review_rating'] = rating_star
					dic['review_content']=review_text
					dic['review_time'] = review_time
					dic['rating_label'] = rating_label
					content_list.append(dic)
				else: 
					continue
			item["reviews"] = content_list
			item["db_name"] =db_name
			yield item
			print("抓取结束")
				
		except Exception as error:
			exception_count+=1
			print(error)
			print("review get error")


		



