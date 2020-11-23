import scrapy
from ..items import WanfangItem

class WanfangdataSpider(scrapy.Spider):
    name = 'wanfangdata'
    allowed_domains = ['www.wanfangdata.com.cn']
    keyword = input()  # 输入关键词匹配
    while not keyword:
        keyword = input("请输入关键词")
    start_urls = [f'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=all&pageSize=50&page=1&searchWord={keyword}&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&corePerio=false&alreadyBuyResource=false&rangeParame=']

    def parse(self, response):
        with open('fi.html', 'wb')as f:
            f.write(response.body)

        ResultList = response.xpath('''////div[@class="ResultList "]/div[2]''')  #获取每个列表集

        #循环列表获取单个数据
        for i in ResultList:
            Item = WanfangItem()
            Item['author'] = i.xpath('div[3]/div[1]/a/text()').getall()  #作者
            Item['Title'] = i.xpath('div[1]/a[1]/text()').getall()   #标题
            Item['URL'] = "http://www.wanfangdata.com.cn" + i.xpath('''div[1]/a[1]/@href''').get()  #URL
            Item['abstr'] = i.xpath('div[4]/text()').get()  #摘要
            Item['Volume'] = i.xpath('div[3]/div[4]/a/text()').getall()   # 期刊日期
            Item['keyword'] = i.xpath('div[5]/a/text()').getall()  # 关键词
            Item['Source'] = i.xpath('div[3]/div[2]/a/text()').getall()   # 来源
            maker = i.xpath('''div[6]//a[@class="result_new_opera_otherWay"]/span/text()''').getall()
            Item['maker'] = maker[0] if maker else None  # 被引用
            Item['download'] = maker[-1] if maker else None  # 下载
            yield Item

        now = int(response.xpath('//*[@id="pageNum"]/@value').get()) #当前页数
        total = int(response.xpath('//*[@id="pageTotal"]/@value').get()) # 总页数
        print(now == total)
        if now == total:  #当前页数等于总页数 结束请求
            return
        now += 1
        url = self.start_urls[0].replace('page=1','page='+str(now))  #请求 页数+1
        yield scrapy.Request(url=url, callback=self.parse)

