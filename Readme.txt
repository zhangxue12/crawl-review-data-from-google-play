method to use this program:
firstly according to the app you want, write dwon the url.
Then open cmd， cd into the project folder, and then input the command, just like:
(1)Zoom
scrapy crawl gp -a urls="https://play.google.com/store/apps/details?id=us.zoom.videomeetings&showAllReviews=true&hl=en"
(2)ding talk
scrapy crawl gp -a urls="https://play.google.com/store/apps/details?id=com.alibaba.android.rimet&showAllReviews=true&hl=en"
(3) Hangouts Meet
scrapy crawl gp -a urls="https://play.google.com/store/apps/details?id=com.google.android.apps.meetings&showAllReviews=true&hl=en"

Most important, you need use goole browser and goole driver, and modify the address of them in config.py.
The last one, this project use mongodb to store data, and you need to change the configure of mongodb in the related files.

