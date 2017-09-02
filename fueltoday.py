import scrapy
import datetime

def beautifyJSON(cities, vals, fuels, sliceInd):
	rate=[]
	for index, city in enumerate(cities):
		obj = {'date': str(datetime.date.today()), 'city': city, 'fuel': []}
		for ind, fuel in enumerate(fuels):
			obj['fuel'].append({'type': fuel, 'value': vals[index+sliceInd*ind]})
		rate.append(obj)
	return rate

class SpiderForRefinery(scrapy.Spider):
	name = "refinery_spider"
	start_urls = ['https://www.iocl.com/TotalProductList.aspx']

	def parse(self, response):
		cities = []
		values = []
		fuel_types = []
		slice_index = 78
		# slice_before = 'Declared as Kerosene-free city'
		FUEL_TYPE_SELECTOR = '#main-body > div.inner-main > div.content'
		PRICE_SELECTOR = '#main-body > div.inner-main > div.content div.product-table-section table.product-table'
		for responseset in response.css(FUEL_TYPE_SELECTOR):
			FUEL_SELECTOR = 'h2[title="Indane"] ::text'
			fuel_types.extend(responseset.css(FUEL_SELECTOR).extract()[:2])
		for responseset in response.css(PRICE_SELECTOR):
			CITY_NAME_SELECTOR = 'tr > td:nth-child(1) ::text'
			VALUE_SELECTOR = 'tr > td:nth-child(2) ::text'
			cities.extend(responseset.css(CITY_NAME_SELECTOR).extract())
			values.extend(responseset.css(VALUE_SELECTOR).extract())
		cities = cities[:slice_index/2]
		values = values[:slice_index]
		yield {'store': beautifyJSON(cities, values, fuel_types, slice_index/2)}
