import pymysql

class Database:
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             database='stu',
                             charset='utf8')

        # 生成游标对象 (操作数据库,执行sql语句,获取结果)
        self.cur = self.db.cursor()

    def close(self):
        # 关闭游标和数据库连接
        self.cur.close()
        self.db.close()

    def register(self,name,passwd):
        pass

    def login(self,name,passwd):
        pass

if __name__ == '__main__':
    db = Database()
    db.register('Tom','123')
    db.login('Tom','123')
    db.close()
