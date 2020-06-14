import pymysql
import os,sys
import json
import configparser
class OperateSQL(object):
    def __init__(self,configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        #连接数据库
        self.conn = pymysql.connect(host=config['mysql']['host'],
                user=config['mysql']['user'],
                passwd=config['mysql']['password'],
                port=int(config['mysql']['port']),
                db=config['mysql']['db'],
                charset=config['mysql']['charset']
                )
        #创建游标对象
        self.cursor = self.conn.cursor()
	
    def create_db(self,name,charset='utf8',collate='utf8_general_ci'):
        '''
        功能：创建一个数据库
        参数：name表示要创建数据表的名称；
        '''
        all_databases = self.show_databases()
        if name.lower() in all_databases:
            print("数据库{}已经被创建！".format(name))
            return
        try:
            self.cursor.execute('create database if not exists ' + name + ' default charset ' + charset + 'collate ' + collate)
            print('创建数据库"{}"成功！'.format(name))
            return 0
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def show_databases(self):
        '''
        功能：查看已创建的数据库
        '''
        try:
            self.cursor.execute('show databases')
            result = []
            while True:
                res = self.cursor.fetchone() 
                if res is None:
                    return result
                result.append(res[0])
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))

    
    def select_database(self,database):
        '''
        功能：选择连接或者修改连接的数据库
        参数：database表示要连接的数据库名称
        '''
        try:
            self.conn.select_db(database)
            return 0
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def delete_database(self,databaseName):
        '''
        功能：删除指定的数据库
        参数：databaseName表示要删除的数据库名称
        '''

        if databaseName not in self.show_databases():
            print('要删除的数据库"{}"不存在!'.format(databaseName))
            return 
        try:
            self.cursor.execute('drop database ' + databaseName)
            print('删除数据库"{}"成功！'.format(databaseName))
            return 0
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def check_current_database(self):
        '''
        功能：查看当前使用的数据库
        '''
        try:
            self.cursor.execute('select database()')
            return self.cursor.fetchone()[0] #返回当前使用数据库的名称
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def create_table(self,tableName,command):
        '''
        功能：创建数据表
        参数：name表示要创建数据表的名称；command表示创建数据表时，定义各字段的详细参数等。
        '''
        all_tables = self.show_tables() #生成器赋值给all_tables变量
        for name in all_tables:
            if tableName.lower() == name: #遍历当前数据库中的数据表生成器，判断是否存在相同名称的数据表
                print('数据表{}已经被创建！'.format(tableName))
                return
        try:
            self.cursor.execute('create table ' + tableName + command)
            print('创建数据表"{}"成功！'.format(tableName))
            return 0
        except pymysql.Error as e:

            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def delete_table(self,tableName):
        '''
        功能：删除指定数据表
        参数：tableName表示要删除的数据表名称
        '''
        all_tables = self.show_tables() #生成器赋值给all_tables变量
        for name in all_tables:
            if tableName == name: #遍历当前数据库中的数据表生成器，判断是否存在相同名称的数据表
                try:
                    self.cursor.execute('drop table ' + tableName)
                    print('删除数据表"{}"成功！'.format(tableName))
                    return 0
                except pymysql.Error as e:
                    print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
        print('要删除的数据表"{}"不存在，请确认并重新删除！'.format(tableName))
    
    def show_tables(self):
        '''
        功能：查看当前数据库中有哪些已创建的数据表，以生成器的方式返回
        '''
        try:
            if self.check_current_database() == None:
                print("请先选择数据库！")
                return
            self.cursor.execute('show tables')
            res = self.cursor.fetchone()
            while res:
                yield res[0] #当res值不为None时，以生成器的方式返回(防止数据库中数据表太多)
                res = self.cursor.fetchone()
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))


    def insert_delete_updata_data(self,command):
        '''
        功能：向数据表中增加或删除或更新数据
        参数：command表示要执行的修改数据的命令
        '''
        try:
            if self.check_current_database() == None:
                print("请先选择数据库！")
                return
            self.cursor.execute(command)
            return 0
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def get_data_from_table(self,command):
        '''
        功能：从数据表中获取数据,以生成器的形式返回
        参数：command表示要执行获取数据的命令;
        '''
        if self.check_current_database() == None:
            print("请先选择数据库！")
            return
        try:
            self.cursor.execute(command)
            res = self.cursor.fetchall()
            for element in res:
                yield element  #防止数据表中有大量的数据，以生成器的方式返回每一项数据
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def commit_database(self):
        '''
        功能：确认并提交数据
        '''
        try:
            self.conn.commit()
            return 0 
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def rollback_database(self):
        '''
        功能：对数据库执行回滚操作
        '''
        try:
            self.conn.rollback()
            return 0 
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
    
    def close_database(self):
        '''
        功能：关闭并退出数据库
        '''
        try:
            self.cursor.close()
            self.conn.close()
            return 0
        except pymysql.Error as e:
            print('Mysql Error %d: %s' %(e.args[0],e.args[1]))
			
class DB():
    def __init__(self, host='localhost', port=3306, db='', user='root', passwd='root', charset='utf8'):
        # 建立连接 
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型        
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标        
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行        
        self.conn.commit()
        # 关闭游标        
        self.cur.close()
        # 关闭数据库连接        
        self.conn.close()
			

if __name__ == '__main__':
	'''
	configpath="config.ini"
	conf= configparser.ConfigParser()
	conf.read(configpath)
	sections = conf.sections()
	print('获取配置文件所有的section', sections)
	options = conf.options('mysql')
	print('获取指定section下所有option', options)
	items = conf.items('mysql')
	print('获取指定section下所有的键值对', items)
	value = conf.get('mysql', 'host')
	print('获取指定的section下的option', type(value), value)
	print(conf['mysql']['host'])
	'''
'''
db = pymysql.connect("localhost","root","123456","Demo" )
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute() 方法执行 SQL，如果表存在则删除
#cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")


sql = "INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s',  %s,  '%s',  %s)" % \
       ('Mac', 'Mohan', 20, 'M', 2000)


sql2 = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
   db.rollback()
   
sql = "SELECT * FROM EMPLOYEE \
       WHERE INCOME > %s" % (1000)
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
       # 打印结果
      print ("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
             (fname, lname, age, sex, income ))
except:
   print ("Error: unable to fetch data")
 
# 关闭数据库连接
db.close()
'''
with DB(host='',user='root',passwd='123456',db='db') as db:
     db.execute('select * from ssm_user')
     #print(db)
     for i in db:
         print(i)

opdb=OperateSQL("config.ini")
tabs=opdb.show_tables()
tables=[]
for item in tabs:
	tables.append(item)
	print(item)
print(tables[3])
commd='select %s from %s where %s=%d' %('username',tables[3],'id',11)
datas=opdb.get_data_from_table(commd)
for data in datas:
	print(data)