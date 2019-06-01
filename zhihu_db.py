# *-* coding:utf8 *-*
from sqlalchemy.inspection import inspect
import db_tables


class ZhihuDb(object):
    def __init__(self):
        db_tables.Base.metadata.reflect(db_tables.engine)
        self.tables = db_tables.Base.metadata.tables
        self.session = db_tables.session
        self.conn = db_tables.engine.connect()

    def __del__(self):
        pass

    def update_table(self, *args, **kw):
        try:
            tablename = args[0]
        except IndexError:
            raise TypeError("update_table() takes at least one argument for tablename")
        try:
            table = self.tables[tablename]
        except KeyError:
            raise TypeError("tablename %s not in database" % tablename)
        table_info = inspect(table)
        primary_keys = [key.name for key in table_info.primary_key]
        records = self.session.query(table)
        for key in primary_keys:
            if key in kw:
                records = records.filter_by(**{key:kw[key]})
        record = records.first()
        if not record:
            print('insert record')
            sql = table.insert().values(**kw)
        else:
            print('update record')
            sql = table.update().values(**kw)
            for key in primary_keys:
                sql = sql.where(table.c.__getattr__(key)==kw[key])
        print(sql)
        self.conn.execute(sql)


if __name__ == '__main__':
    db = ZhihuDb()
    db.update_table("UserCount", user_id='f8ab46045c5a07ac2a3d3e1b2e058692', answer_count=23, question_count=124, articles_count=12)
    db.update_table("UserCount", user_id='f8ab46045c5a07ac2a3d3e1b2e058692', answer_count=23, question_count=124, articles_count=1132)
    db.update_table("UserInfo", user_id='f8ab46045c5a07ac2a3d3e1b2e058692', user_name='浮云dalao', headline='IT工程师/音乐爱好者')
    db.update_table("UserInfo", user_id='q8ab46045c5a07ac2a3d3e1b2e058692', user_name='浮云NBqqq', headline='IT工程师/音乐爱好者qsdf')
    db.update_table("UserInfo", user_id='f8ab46045c5a07ac2a3d3e1b2e058692', user_name='浮云NBqqq', headline='IT工程师/音乐爱好者qqwr')
    db.update_table("UserFollowing", user_id='f8ab46045c5a07ac2a3d3e1b2e058692', following_id='f8ab46045c5a07ac2a3d3e1b2e058693')
    db.update_table("UserFollowing", user_id='f8ab46045c5a07ac2a3d3e1b2e058692', following_id='f8ab46045c5a07ac2a3d3e1b2e058693')
    db.update_table("UserFollowing", user_id='f8ab46045c5a07ac2a3d3e1b2e058691', following_id='f8ab46045c5a07ac2a3d3e1b2e058694')
    db.update_table("UserFollowing", user_id='f8ab46045c5a07ac2a3d3e1b2e058695', following_id='f8ab46045c5a07ac2a3d3e1b2e058693')
    db.update_table("UserCount", user_id='a8ab46045c5a07ac2a3d3e1b2e058692', answer_count=23, question_count=124, articles_count=15)
