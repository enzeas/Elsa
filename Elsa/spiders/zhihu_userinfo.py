# -*- coding: utf-8 -*-
import json
import scrapy
import time
import config
from zhihu_db import ZhihuDb


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    headers = {'user-agent': config.USER_AGENT}
    cookies = config.cookies
    allowed_domains = config.ALLOWED_DOMAINS
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
        to_scrapy_name = []
        for _name, info in users.items():
            if 'uid' in info:
                continue
            if _name == _user_name:
                if 'followingCount' not in info:
                    return
                # TODO(enzo): catch exception
                self.save_user_info(_name, info)
                self.save_user_count(info)
                continue
            #print(_name, info)
            self.save_user_info(_name, info)
            self.save_user_count(info)
            following_id = info['id']
            following_name = info['name']
            self.db.update_table("UserFollowing",user_id=_user_id, following_id=following_id)
            if self.check_scrapy_condition(info):
                to_scrapy_name.append(_name)
        if 'page' in response.url:
            return
        for page_idx in range(1, following_count // 20 + 1):
            url = '{}?page={}'.format(response.url, page_idx + 1)
            time.sleep(config.SLEEP_TIME)
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=self.headers, cookies=self.cookies)
        for _name in to_scrapy_name:
            url = 'https://www.zhihu.com/people/{}/following'.format(_name)
            time.sleep(config.SLEEP_TIME)
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=self.headers, cookies=self.cookies)

    def check_scrapy_condition(self, info):
        if info['userType'] == 'people':
            if info['answerCount'] > 10 and info['followerCount'] > 10:
                return True
        return False

    def save_user_info(self, _name, info):
        print(info)
        user_id = info['id']
        user_name = _name
        nick_name = info['name']
        avatar_url = info['avatarUrl']
        avatar_url_template = info['avatarUrlTemplate']
        headline = info['headline']
        user_type = info['userType']
        business = info['business']['name'] if 'business' in info and 'name' in info['business'] else ''
        educations = info['educations'][0]['school']['name'] if 'educations' in info and len(info['educations']) and 'school' in info['educations'][0] and 'name' in info['educations'][0]['school'] else ''
        employments = info['employments'][0]['company']['name'] if 'employments' in info and len(info['employments']) and 'company' in info['employments'][0] and 'name' in info['employments'][0]['company'] else ''
        locations = info['locations'][0]['name'] if 'locations' in info and len(info['locations']) and 'name' in info['locations'][0] else ''
        gender = info['gender']
        description = info.get('description', '')
        type = info['type']
        url = info['url']
        url_token = info['urlToken']
        self.db.update_table("UserInfo", user_id=user_id, user_name=user_name, nick_name=nick_name,
            avatar_url=avatar_url, avatar_url_template=avatar_url_template,
            headline=headline, user_type=user_type, business=business, educations=educations, employments=employments,
            locations=locations, gender=gender, description=description, type=type, url=url, url_token=url_token)

    def save_user_count(self, info):
        user_id = info['id']
        answer_count = info['answerCount']
        question_count = info.get('questionCount', 0)
        articles_count = info.get('articlesCount', 0)
        columns_count = info.get('columnsCount', 0)
        pins_count = info.get('pinsCount', 0)
        favorite_count = info.get('favoriteCount', 0)
        voteup_count = info.get('voteupCount', 0)
        thanked_count = info.get('thankedCount', 0)
        favorited_count = info.get('favoritedCount', 0)
        logs_count= info.get('logsCount', 0)
        following_count = info.get('followingCount', 0)
        follower_count = info.get('followerCount', 0)
        participated_live_count = info.get('participatedLiveCount', 0)
        following_columns_count = info.get('followingColumnsCount', 0)
        following_favlists_count = info.get('followingFavlistsCount', 0)
        following_question_count = info.get('followingQuestionCount', 0)
        following_topic_count = info.get('followingTopicCount', 0)
        commercial_question_count = info.get('commercialQuestionCount', 0)
        hosted_live_count = info.get('hostedLiveCount', 0)
        included_answers_count = info.get('includedAnswersCount', 0)
        included_articles_count = info.get('includedArticlesCount', 0)
        mutual_followees_count = info.get('mutualFolloweesCount', 0)
        thank_from_count = info.get('thankFromCount', 0)
        thank_to_count = info.get('thankToCount', 0)
        vote_from_count = info.get('voteFromCount', 0)
        vote_to_count = info.get('voteToCount', 0)
        self.db.update_table("UserCount", user_id=user_id,
            answer_count=answer_count, question_count=question_count,
            articles_count=articles_count, columns_count=columns_count,
            pins_count=pins_count, favorite_count=favorite_count,
            voteup_count=voteup_count, thanked_count=thanked_count,
            favorited_count=favorited_count, logs_count=logs_count,
            following_count=following_count, follower_count=follower_count,
            participated_live_count=participated_live_count,
            following_columns_count=following_columns_count,
            following_favlists_count=following_favlists_count,
            following_question_count=following_question_count,
            following_topic_count=following_topic_count,
            commercial_question_count=commercial_question_count,
            hosted_live_count=hosted_live_count,
            included_answers_count=included_answers_count,
            included_articles_count=included_articles_count,
            mutual_followees_count=mutual_followees_count,
            thank_from_count=thank_from_count, thank_to_count=thank_to_count,
            vote_from_count=vote_from_count, vote_to_count=vote_to_count)
