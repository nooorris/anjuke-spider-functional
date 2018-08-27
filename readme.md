this is the scraper program for house price data in Fuzhou

this program gets the house data from www.Anjuke.com
remove those unnecessary items
group those remained items in terms of estates (by location)
get the longitude and latitude of estates and mark them in Baidu Map
when click the mark, the availible house in that housing estate will be listed with basic information as below:
[indicator],area,price,year,room&lounge,floor,unit_price,link
the link connect the website with detailed information of that item

to prevent the anti-scraper approaches of www.Anjuke.com, following actions were taken:
1. request with user agent,cookies and other header infromation 
2. realtime proxy pool from www.xicidaili.com with automatic update
3. scraping with controlled pausing time

# This is my first scraper program. Welccome feedback and report bug by launching issues
