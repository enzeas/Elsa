# -*- coding: utf-8 -*-
import json
import scrapy
import config


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    cookies = config.cookies
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/people/de-lu-shan']

    def start_requests(self):
        for base_url in self.start_urls:
            url = base_url + '/following'
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        print(response.url)
        foo = response.xpath('//script[@id="js-initialData"]/text()').extract_first()
        bar = json.loads(foo)
        users = bar['initialState']['entities']['users']
        user_id = bar['initialState']['currentUser']
        user_name = response.url.split('/')[-2]
        following_count = 0
        # TODO: save to sql
        to_scrapy_name = []
        filename = '{}/{}'.format(config.data_path, user_name)
        with open(filename, 'a') as f:
            for _name, info in users.items():
                if _name == user_id:
                    continue
                if _name == user_name:
                    if 'followingCount' not in info:
                        return
                    following_count = info['followingCount']
                    continue
                id = info['id']
                name = info['name']
                avatar = info['avatarUrlTemplate'].format(size='xl')
                user_type = info['userType']
                headline = info['headline']
                gender = info['gender']
                answer_count = info['answerCount']
                articles_count = info['articlesCount']
                follower_count = info['followerCount']
                f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(id, name, avatar, headline, user_type, gender, answer_count, articles_count, follower_count))
                if user_type == 'people':
                    # TODO: active user
                    if answer_count > 10 and follower_count > 10:
                        to_scrapy_name.append(_name)
        if 'page' in response.url:
            return
        for page_idx in range(1, following_count // 20 + 1):
            url = '{}?page={}'.format(response.url, page_idx + 1)
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)
        for _name in to_scrapy_name:
            url = 'https://www.zhihu.com/people/{}/following'.format(_name)
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)
