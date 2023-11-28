# -*- coding: utf-8 -*-
import scrapy

from scrapy.crawler import CrawlerProcess
import json
import logging
class ExampleSpider(scrapy.Spider):
    with open("../lat_lon_q1.json", 'r') as json_file:
        datas = json.load(json_file)
    name = 'example'
    allowed_domains = []
    # start_urls = ['https://nominatim.openstreetmap.org/reverse?lat={}&lon={}&format=jsonv2'.format(i['lat'], i['lon']) for i in datas]
    # start_urls = ['https://api-app.map4d.vn/map/geocode?lat={}&lng={}'.format(i['lat'], i['lon']) for i in datas]
    start_urls = ['https://jsonplaceholder.typicode.com/todos/{}'.format(i) for i in range(1, 201)]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.error_handler)

    def parse(self, response):
   
        data = json.loads(response.text)
        data['req']=response.request.url
        # print(">>>>",data)
        pretty_data = json.dumps(data, indent=4)

        # Đọc dữ liệu hiện tại từ file (nếu có)
        current_data = []
        try:
            with open('crawl_q1_v2.json', 'r') as file:
                current_data = json.load(file)
        except FileNotFoundError:
            pass  # Nếu file không tồn tại, tiếp tục với mảng trống
        # Thêm dữ liệu mới vào mảng hiện tại
        current_data.append(data)
        # print('>>>>>>>',current_data)
        # Ghi mảng vào file
        with open('crawl_q1_v2.json', 'w') as file:
            json.dump(current_data, file, indent=4, ensure_ascii=False)
        # print(pretty_data)

    def error_handler(self, failure):
        request_url = failure.request.url
        status_code = failure.value.response.status
        logging.error(f"An error occurred for URL {request_url}: Status Code {status_code}")
        current_data = []
        try:
            with open('400_cong.json', 'r') as file:
                current_data = json.load(file)
        except FileNotFoundError:
            pass  # Nếu file không tồn tại, tiếp tục với mảng trống

        # Thêm dữ liệu mới vào mảng hiện tại
        current_data.append({'errapi': request_url, 'status': status_code})

        # Ghi mảng vào file
        with open('400_cong.json', 'w') as file:
            json.dump(current_data, file, indent=4)

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ExampleSpider)
    process.start()

