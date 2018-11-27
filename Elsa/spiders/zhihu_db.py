#!/usr/bin/env python3
import mysql.connector


class ZhihuDb(object):
    def __init__(self):
        self.db = mysql.connector.connect(
            host="193.112.104.49",
            user="root",
            passwd="eeaa666",
            database="zhihu"
        )
    def __del__(self):
        self.db.commit()

    def update_user_count(self, id='', answer_count=0, question_count=0,
            articles_count=0, columns_count=0, pins_count=0, favorite_count=0,
            voteup_count=0, thanked_count=0, favorited_count=0, logs_count=0,
            following_count=0, follower_count=0, participated_live_count=0,
            following_columns_count=0, following_favlists_count=0,
            following_question_count=0, following_topic_count=0,
            commercial_question_count=0, hosted_live_count=0,
            included_answers_count=0, included_articles_count=0, mutual_followees_count=0,
            thank_from_count=0, thank_to_count=0, vote_from_count=0, vote_to_count=0):
        cursor = self.db.cursor()
        sql = ('replace into UserCount (id, answerCount, questionCount, ' # 3
               'articlesCount, columnsCount, pinsCount, favoriteCount, ' # 4
               'voteupCount, thankedCount, favoritedCount, logsCount, ' # 4
               'followingCount, followerCount, participatedLiveCount, ' # 3
               'followingColumnsCount, followingFavlistsCount, ' # 2
               'followingQuestionCount, followingTopicCount, ' # 2
               'commercialQuestionCount, hostedLiveCount, ' # 2
               'includedAnswersCount, includedArticlesCount, mutualFolloweesCount, ' # 3
               'thankFromCount, thankToCount, voteFromCount, voteToCount) ' # 4
               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' # 14 %s
               '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)') # 13 %s
        val = (id, answer_count, question_count,
               articles_count, columns_count, pins_count, favorite_count,
               voteup_count, thanked_count, favorited_count, logs_count,
               following_count, follower_count, participated_live_count,
               following_columns_count,following_favlists_count,
               following_question_count, following_topic_count,
               commercial_question_count, hosted_live_count,
               included_answers_count, included_articles_count, mutual_followees_count,
               thank_from_count, thank_to_count, vote_from_count, vote_to_count)
        #print(sql % val)
        cursor.execute(sql, val)
        self.db.commit()

    def update_user_info(self, id='', name='', avatar_url='', avatar_url_template='',
            headline='', user_type='', business='', educations= '', employments='',
            locations='', gender=0, description='', type='', url='', url_token=''):
        cursor = self.db.cursor()
        # TODO(enzo): use if statement
        sql = ('replace into UserInfo (id, name, avatarUrl, avatarUrlTemplate, '
               'headline, userType, business, educations, employments, '
               'locations, gender, description, type, url, urlToken) '
               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ')
        val = (id, name, avatar_url, avatar_url_template,
               headline, user_type, business, educations, employments,
               locations, gender, description, type, url, url_token,)
        #print(sql % val)
        cursor.execute(sql, val)
        self.db.commit()

    def update_user_following(self, id='', following='', name='', following_name=''):
        sql = ('replace into UserFollowing (id, following, name, followingName) '
               'values (%s, %s, %s, %s)')
        val = (id, following, name, following_name)
        cursor = self.db.cursor()
        cursor.execute(sql, val)
        self.db.commit()


if __name__ == '__main__':
    db = ZhihuDb()
    db.update_user_count(id='f8ab46045c5a07ac2a3d3e1b2e058692', answer_count=23, question_count=124, articles_count=12)
    db.update_user_count(id='f8ab46045c5a07ac2a3d3e1b2e058692', answer_count=23, question_count=124, articles_count=1132)
    db.update_user_info(id='f8ab46045c5a07ac2a3d3e1b2e058692', name='浮云dalao', headline='IT工程师/音乐爱好者')
    db.update_user_info(id='q8ab46045c5a07ac2a3d3e1b2e058692', name='浮云NBqqq', headline='IT工程师/音乐爱好者qsdf')
    db.update_user_info(id='f8ab46045c5a07ac2a3d3e1b2e058692', name='浮云NBqqq', headline='IT工程师/音乐爱好者qqwr')
