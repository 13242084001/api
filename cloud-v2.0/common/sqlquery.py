import pymysql.cursors
import json

class Query(object):
    def __init__(self):

        # 连接数据库
        self.connection = pymysql.connect(host='172.16.130.254',
                                         user='root',
                                         password='123456',
                                         db='cloudadmin',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

    def __call__(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
        finally:
            self.connection.close()


#sql_result = Query()("SELECT * FROM `cl_volume_inf` where STATE = 0 and VMID is null;")
