# *-* coding:utf8 *-*
from datetime import datetime
from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///db/zhihu.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# *default value* for this column will be invoked upon insert
class UserInfo(Base):
    __tablename__ = 'UserInfo'
    user_id = Column(String(32), default='', primary_key=True)
    user_name = Column(String(32), default='')
    nick_name = Column(String(32), default='')
    avatar_url = Column(String(128), default='')
    avatar_url_template = Column(String(128), default='')
    headline = Column(String(255), default='')
    user_type = Column(String(32), default='')
    business = Column(String(255), default='')
    educations = Column(String(255), default='')
    employments = Column(String(255), default='')
    locations = Column(String(255), default='')
    gender = Column(Integer, default=0)
    description = Column(String(255), default='')
    type = Column(String(255), default='')
    url = Column(String(255), default='')
    url_token = Column(String(255), default='')

    def __repr__(self):
        return ("UserInfo(user_id='%s', user_name='%s', nick_name='%s', "
                "avatar_url='%s', avatar_url_template='%s')" % (
                self.user_id, self.user_name, self.nick_name,
                self.avatar_url, self.avatar_url_template))

class UserCount(Base):
    __tablename__ = 'UserCount'
    user_id = Column(String(32), default='', primary_key=True)
    answer_count = Column(Integer, default=0)
    question_count = Column(Integer, default=0)
    articles_count = Column(Integer, default=0)
    columns_count = Column(Integer, default=0)
    pins_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    voteup_count = Column(Integer, default=0)
    thanked_count = Column(Integer, default=0)
    favorited_count = Column(Integer, default=0)
    logs_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    follower_count = Column(Integer, default=0)
    participated_live_count = Column(Integer, default=0)
    following_columns_count = Column(Integer, default=0)
    following_favlists_count = Column(Integer, default=0)
    following_question_count = Column(Integer, default=0)
    following_topic_count = Column(Integer, default=0)
    commercial_question_count = Column(Integer, default=0)
    hosted_live_count = Column(Integer, default=0)
    included_answers_count = Column(Integer, default=0)
    included_articles_count = Column(Integer, default=0)
    mutual_followees_count = Column(Integer, default=0)
    thank_from_count = Column(Integer, default=0)
    thank_to_count = Column(Integer, default=0)
    vote_from_count = Column(Integer, default=0)
    vote_to_count = Column(Integer, default=0)

    def __repr__(self):
        return ("UserCount(user_id='%s', answer_count='%d', "
                "question_count='%d', articles_count='%d'" % (
                self.user_id, self.answer_count,
                self.question_count, self.articles_count))

class UserFollowing(Base):
    __tablename__ = 'UserFollowing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(32), default='')
    user_name = Column(String(32), default='')
    following_id = Column(String(32), default='')
    following_name = Column(String(32), default='')

    def __repr__(self):
        return ("UserFollowing(user_id='%s', user_name='%s', "
                "following_id='%s', following_name='%s')" % (
                self.user_id, self.user_name,
                self.following_id, self.following_name))


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
