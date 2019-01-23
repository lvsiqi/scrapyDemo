import scrapy
from tenCent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    base_url = 'https://hr.tencent.com/'
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        node_list = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
        # 选取所有标签tr 且class属性等于even或odd的元素
        next_page = response.xpath('//a[@id="next"]/@href').extract_first()
        # 选取所有标签a且id=next,href属性值

        for node in node_list:
            '''
            实例化对象要放在循环里面，否则会造成item被多次赋值，
            因为每次循环完毕后，请求只给了调度器，入队，并没有去执行请求，
            循环完毕后，下载器会异步执行队列中的请求,此时item已经为最后一条记录，
            而详细内容根据url不同去请求的，所以每条详细页是完整的，
            最终结果是数据内容为每页最后一条，详细内容与数据内容不一致，
            在yield item后，会把内容写到pipeline中
            '''
            item = TencentItem()

            item['position_name'] = node.xpath('./td[1]/a/text()').extract_first()  # 获取第一个td标签下a标签的文本
            item['position_link'] = node.xpath('./td[1]/a/@href').extract_first()  # 获取第一个td标签下a标签href属性
            item['position_type'] = node.xpath('./td[2]/text()').extract_first()  # 获取第二个td标签下文本
            item['position_number'] = node.xpath('./td[3]/text()').extract_first()  # 获取第3个td标签下文本
            item['work_location'] = node.xpath('./td[4]/text()').extract_first()  # 获取第4个td标签下文本
            item['publish_times'] = node.xpath('./td[5]/text()').extract_first()  # 获取第5个td标签下文本
            # yield item  注释yield item ，因为detail方法中yield item会覆盖这个
            yield scrapy.Request(url=self.base_url + item['position_link'], callback=self.detail,
                                 meta={'item': item})  # 请求详细页，把item传到detail
            # 请求给调度器，入队，循环结束完成后，交给下载器去异步执行，返回response
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse)  # 请求下一页

    def detail(self, response):
        """
        爬取详细内容
        :param response:
        :return:
        """
        print("-->detail")
        item = response.meta['item']  # 得到parse中的yield item
        item['position_duty'] = ''.join(
            response.xpath('//ul[@class="squareli"]')[0].xpath('./li/text()').extract())  # 转化为字符串
        item['position_require'] = ''.join(
            response.xpath('//ul[@class="squareli"]')[1].xpath('./li/text()').extract())  # 转化为字符串

        yield item
