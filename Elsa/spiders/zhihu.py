# -*- coding: utf-8 -*-
import json
import scrapy
import time
import config
from Elsa.spiders.zhihu_db import ZhihuDb


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    cookies = config.cookies
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/people/de-lu-shan']
    db = ZhihuDb()

    def start_requests(self):
        for base_url in self.start_urls:
            url = base_url + '/following'
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        print(response.url)
        json_info = response.xpath('//script[@id="js-initialData"]/text()').extract_first()
        json_dict = json.loads(json_info)
        users = json_dict['initialState']['entities']['users']
        _user_id = ''
        for _name in json_dict['initialState']['people']['profileStatus']:
            _user_id = json_dict['initialState']['people']['profileStatus'][_name]['token']['id']
        _user_name = response.url.split('/')[-2]
        following_count = 0
        # TODO: save to sql
        to_scrapy_name = []
        #filename = '{}/{}'.format(config.data_path, user_name)
        #with open(filename, 'a') as f:
        for _name, info in users.items():
            if 'uid' in info:
                continue
            if _name == _user_name:
                if 'followingCount' not in info:
                    return
                # TODO(enzo): catch exception
                _this_id = info['id']
                id = info['id']
                name = info['name']
                avatar_url = info['avatarUrl']
                avatar_url_template = info['avatarUrlTemplate']
                headline = info['headline']
                user_type = info['userType']
                #print(info)
                business = info['business']['name'] if 'business' in info and 'name' in info['business'] else ''
                educations = info['educations'][0]['school']['name'] if 'educations' in info and len(info['educations']) and 'school' in info['educations'][0] and 'name' in info['educations'][0]['school'] else ''
                employments = info['employments'][0]['company']['name'] if 'employments' in info and len(info['employments']) and 'company' in info['employments'][0] and 'name' in info['employments'][0]['company'] else ''
                locations = info['locations'][0]['name'] if 'locations' in info and len(info['locations']) and 'name' in info['locations'][0] else ''
                gender = info['gender']
                description = info['description']
                type = info['type']
                url = info['url']
                url_token = info['urlToken']
                self.db.update_user_info(id=id, name=name, avatar_url=avatar_url, avatar_url_template=avatar_url_template,
                    headline=headline, user_type=user_type, business=business, educations=educations, employments=employments,
                    locations=locations, gender=gender, description=description, type=type, url=url, url_token=url_token)
                answer_count = info['answerCount']
                question_count = info['questionCount']
                articles_count = info['articlesCount']
                columns_count = info['columnsCount']
                pins_count = info['pinsCount']
                favorite_count = info['favoriteCount']
                voteup_count = info['voteupCount']
                thanked_count = info['thankedCount']
                favorited_count = info['favoritedCount']
                logs_count= info['logsCount']
                following_count = info['followingCount']
                follower_count = info['followerCount']
                participated_live_count = info['participatedLiveCount']
                following_columns_count = info['followingColumnsCount']
                following_favlists_count = info['followingFavlistsCount']
                following_question_count = info['followingQuestionCount']
                following_topic_count = info['followingTopicCount']
                commercial_question_count = info['commercialQuestionCount']
                hosted_live_count = info['hostedLiveCount']
                included_answers_count = info['includedAnswersCount']
                included_articles_count = info['includedArticlesCount']
                mutual_followees_count = info['mutualFolloweesCount']
                thank_from_count = info['thankFromCount']
                thank_to_count = info['thankToCount']
                vote_from_count = info['voteFromCount']
                vote_to_count = info['voteToCount']
                self.db.update_user_count(id, answer_count, question_count,
                    articles_count, columns_count, pins_count, favorite_count,
                    voteup_count, thanked_count, favorited_count, logs_count,
                    following_count, follower_count, participated_live_count,
                    following_columns_count,following_favlists_count,
                    following_question_count, following_topic_count,
                    commercial_question_count, hosted_live_count,
                    included_answers_count, included_articles_count, mutual_followees_count,
                    thank_from_count, thank_to_count, vote_from_count, vote_to_count)
                continue
            #print(_name, info)
            user_id = info['id']
            name = info['name']
            avatar_url = info['avatarUrl']
            avatar_url_template = info['avatarUrlTemplate']
            headline = info['headline']
            user_type = info['userType']
            gender = info['gender']
            type = info['type']
            url = info['url']
            url_token = info['urlToken']
            answer_count = info['answerCount']
            articles_count = info['articlesCount']
            follower_count = info['followerCount']
            self.db.update_user_info(id=user_id, name=name, avatar_url=avatar_url,
                    avatar_url_template=avatar_url_template, headline=headline,
                    user_type=user_type, gender=gender,
                    type=type, url=url, url_token=url_token)
            self.db.update_user_count(id=user_id, answer_count=answer_count,
                    articles_count=articles_count, follower_count=follower_count)
            self.db.update_user_following(id=_user_id, following=user_id, name=_user_name, following_name=name)
            if user_type == 'people':
                # TODO: active user
                if answer_count > 10 and follower_count > 10:
                    to_scrapy_name.append(_name)
            #f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(user_id, name, avatar, headline, user_type, gender, answer_count, articles_count, follower_count))
        if 'page' in response.url:
            return
        for page_idx in range(1, following_count // 20 + 1):
            url = '{}?page={}'.format(response.url, page_idx + 1)
            time.sleep(0.5)
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=self.headers, cookies=self.cookies)
        for _name in to_scrapy_name:
            url = 'https://www.zhihu.com/people/{}/following'.format(_name)
            time.sleep(0.5)
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=self.headers, cookies=self.cookies)
