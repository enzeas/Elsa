# -*- coding: utf-8 -*-
import json
import scrapy
import time
import config
from zhihu_db import ZhihuDb


class ZhihuQuestion(scrapy.Spider):
    name = 'zhihu_question'
    headers = {'user-agent': config.USER_AGENT}
    cookies = config.cookies
    allowed_domains = config.ALLOWED_DOMAINS
    start_url = 'https://www.zhihu.com/hot'
    db = ZhihuDb()

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_hot_page,
                             headers=self.headers, cookies=self.cookies)
        #yield scrapy.Request(url='https://www.zhihu.com/question/326780069',
        #        callback=self.parse_question, headers=self.headers, cookies=self.cookies)


    def parse_hot_page(self, response):
        #print(response.url)
        json_info = response.xpath('//script[@id="js-initialData"]/text()').extract_first()
        json_dict = json.loads(json_info)
        hot_list = json_dict['initialState']['topstory']['hotList']
        for info in hot_list:
            target = info['target']
            link = self.save_hot_question(target)
            yield scrapy.Request(url=link, callback=self.parse_question,
                                 headers=self.headers, cookies=self.cookies)

    def parse_question(self, response):
        #print(response.url)
        json_info = response.xpath('//script[@id="js-initialData"]/text()').extract_first()
        json_dict = json.loads(json_info)
        questions = json_dict['initialState']['entities']['questions']
        for q, question in questions.items():
            question_url = self.save_question(question)
            answer_url = question_url + '/answers?limit=20&offset=0&sort_by=default&platform=desktop&'
            include = 'include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics'
            # default limit 5 offset 0 max 20
            time.sleep(config.SLEEP_TIME)
            yield scrapy.Request(url=answer_url + include, callback=self.parse_answer,
                                 headers=self.headers, cookies=self.cookies)

    def parse_answer(self, response):
        #print(response.url)
        json_dict = json.loads(response.text)
        answers = json_dict['data']
        for answer in answers:
            answer_url = self.save_answer(answer)
            comment_url = answer_url + '/root_comments?limit=20&offset=0&order=normal&status=open'
            # default limit 5 offset 0 max 20
            time.sleep(config.SLEEP_TIME)
            yield scrapy.Request(url=comment_url, callback=self.parse_comment,
                                 headers=self.headers, cookies=self.cookies)

    def parse_comment(self, response):
        #print(response.url)
        answer_id = int(response.url.split('/')[6])
        json_dict = json.loads(response.text)
        comments = json_dict['data']
        for comment in comments:
            comment_url = self.save_comment(comment, answer_id)
            child_url = comment_url + '/child_comments'
            # default all ?
            time.sleep(config.SLEEP_TIME)
            yield scrapy.Request(url=child_url, callback=self.parse_child,
                                 headers=self.headers, cookies=self.cookies)

    def parse_child(self, response):
        #print(response.url)
        json_dict = json.loads(response.text)
        children = json_dict['data']
        for child in children:
            self.save_child(child)


    def save_hot_question(self, target):
        title = target['titleArea']['text']
        link = target['link']['url']
        metrics = target['metricsArea']['text']
        excerpt = target['excerptArea']['text'] if 'text' in target['excerptArea'] else ''
        image = target['imageArea']['url'] if 'url' in target['imageArea'] else ''
        print(title, link, metrics)
        hash_id = hash(link + metrics)
        hot_time = int(time.time())
        self.db.update_table("HotQuestion", hash_id=hash_id, title=title,
                link=link, metrics=metrics, excerpt=excerpt, image=image,
                hot_time=hot_time)
        return link

    def save_question(self, question):
        # print(question)
        question_id = question['id']
        title = question['title']
        url = question['url']
        author_id = question['author']['id'] # foreign key
        answer_count = question['answerCount']
        visit_count = question['visitCount']
        comment_count = question['commentCount']
        follower_count = question['followerCount']
        created_time = question['created']
        updated_time = question['updatedTime']
        excerpt = question['excerpt']
        detail = question['detail']
        topics = ' '.join([topic['name'] for topic in question['topics']])
        # print(question_id, title, url, topics, excerpt, detail)
        self.db.update_table("QuestionInfo", question_id=question_id,
                title=title, url=url, author_id=author_id,
                answer_count=answer_count, visit_count=visit_count,
                comment_count=comment_count, follower_count=follower_count,
                created_time=created_time, updated_time=updated_time,
                excerpt=excerpt, detail=detail, topics=topics)
        return url

    def save_answer(self, answer):
        answer_id = answer['id']
        url = answer['url']
        question_id = answer['question']['id'] # foreign key
        author_id = answer['author']['id'] # author key
        created_time = answer['created_time']
        updated_time = answer['updated_time']
        # include data
        voteup_count = answer['voteup_count']
        comment_count = answer['comment_count']
        content = answer['content']
        #print(answer_id, voteup_count, comment_count, content)
        self.db.update_table("AnswerInfo", answer_id=answer_id,
                url=url, question_id=question_id, author_id=author_id,
                created_time=created_time, updated_time=updated_time,
                voteup_count=voteup_count, comment_count=comment_count,
                content=content)
        return url

    def save_comment(self, comment, answer_id):
        comment_id = comment['id']
        author_id = comment['author']['member']['id'] # foreign key
        # answer_id # foreign key
        url = comment['url'].replace('comments', 'api/v4/comments')
        created_time = comment['created_time']
        vote_count = comment['vote_count']
        child_comment_count = comment['child_comment_count']
        content = comment['content']
        #print(comment_id, answer_id, vote_count, child_comment_count, content)
        self.db.update_table("CommentInfo", comment_id=comment_id,
                author_id=author_id, answer_id=answer_id,
                url=url, created_time=created_time, content=content,
                vote_count=vote_count, child_comment_count=child_comment_count)
        return url

    def save_child(self, child):
        child_comment_id = child['id']
        author_id = child['author']['member']['id'] # foreign key
        reply_to_author_id = child['reply_to_author']['member']['id'] # foreign key
        created_time = child['created_time']
        vote_count = child['vote_count']
        replies_count = child['replies_count']
        content = child['content']
        #print(comment_id, author_id, reply_to_author_id, content)
        self.db.update_table("ChildCommentInfo", child_comment_id=child_comment_id,
                author_id=author_id, reply_to_author_id=reply_to_author_id,
                content=content, created_time=created_time,
                vote_count=vote_count, replies_count=replies_count)
