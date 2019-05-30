# *-* coding:utf8 *-*
import db_tables
from db_tables import UserCount, UserInfo, UserFollowing


class ZhihuDb(object):
    def __init__(self):
        self.session = db_tables.session
    def __del__(self):
        pass

    # TODO: use **kwargs and setattr
    def update_user_info(self, id='', name='', nick_name='',
            avatar_url='', avatar_url_template='',
            headline='', user_type='', business='', educations= '', employments='',
            locations='', gender=0, description='', type='', url='', url_token=''):
        userinfo = self.session.query(UserInfo).filter_by(user_id=id).first()
        if not userinfo:
            print('insert record')
            userinfo = UserInfo()
            userinfo.user_id=id
            self.session.add(userinfo)
        else:
            print('update record')
        #print(userinfo)
        if name:
            userinfo.user_name = name
        if nick_name:
            userinfo.nick_name = nick_name
        if avatar_url:
            userinfo.avatar_url = avatar_url
        if avatar_url_template:
            userinfo.avatar_url_template = avatar_url_template
        if headline:
            userinfo.headline = headline
        if user_type:
            userinfo.user_type = user_type
        if business:
            userinfo.business = business
        if educations:
            userinfo.educations = educations
        if employments:
            userinfo.employments = employments
        if locations:
            userinfo.locations = locations
        if gender:
            userinfo.gender = gender
        if description:
            userinfo.description = description
        if type:
            userinfo.type = type
        if url:
            userinfo.url = url
        if url_token:
            userinfo.url_token = url_token
        #print(self.session.dirty)
        self.session.commit()

    def update_user_count(self, id='', answer_count=0, question_count=0,
            articles_count=0, columns_count=0, pins_count=0, favorite_count=0,
            voteup_count=0, thanked_count=0, favorited_count=0, logs_count=0,
            following_count=0, follower_count=0, participated_live_count=0,
            following_columns_count=0, following_favlists_count=0,
            following_question_count=0, following_topic_count=0,
            commercial_question_count=0, hosted_live_count=0,
            included_answers_count=0, included_articles_count=0, mutual_followees_count=0,
            thank_from_count=0, thank_to_count=0, vote_from_count=0, vote_to_count=0):
        usercount = self.session.query(UserCount).filter_by(user_id=id).first()
        if not usercount:
            print('insert record')
            usercount = UserCount()
            usercount.user_id=id
            self.session.add(usercount)
        else:
            print('update record')
        if answer_count:
            usercount.answer_count = answer_count
        if question_count:
            usercount.question_count = question_count
        if articles_count:
            usercount.articles_count = articles_count
        if columns_count:
            usercount.columns_count = columns_count
        if pins_count:
            usercount.pins_count = pins_count
        if favorite_count:
            usercount.favorite_count = favorite_count
        if voteup_count:
            usercount.voteup_count = voteup_count
        if thanked_count:
            usercount.thanked_count = thanked_count
        if favorited_count:
            usercount.favorited_count = favorited_count
        if logs_count:
            usercount.logs_count = logs_count
        if following_count:
            usercount.following_count = following_count
        if follower_count:
            usercount.follower_count = follower_count
        if participated_live_count:
            usercount.participated_live_count = participated_live_count
        if following_columns_count:
            usercount.following_columns_count = following_columns_count
        if following_favlists_count:
            usercount.following_favlists_count = following_favlists_count
        if following_question_count:
            usercount.following_question_count = following_question_count
        if following_topic_count:
            usercount.following_topic_count = following_topic_count
        if commercial_question_count:
            usercount.commercial_question_count = commercial_question_count
        if hosted_live_count:
            usercount.hosted_live_count = hosted_live_count
        if included_answers_count:
            usercount.included_answers_count = included_answers_count
        if included_articles_count:
            usercount.included_articles_count = included_articles_count
        if mutual_followees_count:
            usercount.mutual_followees_count = mutual_followees_count
        if thank_from_count:
            usercount.thank_from_count = thank_from_count
        if thank_to_count:
            usercount.thank_to_count = thank_to_count
        if vote_from_count:
            usercount.vote_from_count = vote_from_count
        if vote_to_count:
            usercount.vote_to_count = vote_to_count
        #print(usercount)
        #print(self.session.dirty)
        self.session.commit()

    def update_user_following(self, id='', name='', following_id='', following_name=''):
        userfollowing = self.session.query(UserFollowing).filter_by(user_id=id).filter_by(following_id=following_id).first()
        if not userfollowing:
            print('insert record')
            userfollowing = UserFollowing()
            userfollowing.user_id=id
            self.session.add(userfollowing)
        else:
            print('update record')
        print(userfollowing)
        userfollowing.user_name = name
        userfollowing.following_id = following_id
        userfollowing.following_name = following_name
        #print(self.session.dirty)
        self.session.commit()


if __name__ == '__main__':
    db = ZhihuDb()
    db.update_user_count(id='f8ab46045c5a07ac2a3d3e1b2e058692', answer_count=23, question_count=124, articles_count=12)
    db.update_user_count(id='f8ab46045c5a07ac2a3d3e1b2e058692', answer_count=23, question_count=124, articles_count=1132)
    db.update_user_info(id='f8ab46045c5a07ac2a3d3e1b2e058692', name='浮云dalao', headline='IT工程师/音乐爱好者')
    db.update_user_info(id='q8ab46045c5a07ac2a3d3e1b2e058692', name='浮云NBqqq', headline='IT工程师/音乐爱好者qsdf')
    db.update_user_info(id='f8ab46045c5a07ac2a3d3e1b2e058692', name='浮云NBqqq', headline='IT工程师/音乐爱好者qqwr')
