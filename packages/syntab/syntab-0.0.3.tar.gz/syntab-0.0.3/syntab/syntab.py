#coding=utf-8
from __future__ import division
from __future__ import print_function
import os
import sys
import traceback
import pymysql
import collections
import functools
import logging
import time

logger = logging.getLogger('syntab')


def count_time(is_debug):
    def handle_func(func):
        @functools.wraps(func)
        def handle_args(*args, **kwargs):
            rt = None
            begin = time.time()
            rt = func(*args, **kwargs)
            logger.debug( "[{0}] spend {1}s".format(func.__name__,str(time.time() - begin) ))
            return rt
        return handle_args
    return handle_func

class syntab(object):
    #user:passwd@127.0.0.1:3306
    def __init__(self,source_db,targe_db):
        logging.info("")
        self.s_user,self.s_passwd,self.s_host,self.s_port = self.__parse_db(source_db)
        self.t_user,self.t_passwd,self.t_host,self.t_port = self.__parse_db(targe_db)

    def __parse_db(self,db_str):
        port = 3306
        user,host = tuple(db_str.split('@'))
        user,passwd = tuple(user.split(':'))
        if (len(host.split(':')) == 2):
            port = int(host.split(':')[1])   
            host = host.split(':')[0]        
        return user,passwd,host,port
    
    def __del__(self):
        pass

    
    @count_time(True)
    def syn(self,source_dbname,targe_dbname,tab_name = None):
        db1 = pymysql.connect(host=self.s_host,user=self.s_user,passwd=self.s_passwd,db=source_dbname,port = self.s_port, use_unicode=1,charset='utf8')
        db2 = pymysql.connect(host=self.t_host,user=self.t_user,passwd=self.t_passwd,db=targe_dbname,port = self.t_port, use_unicode=1,charset='utf8')
        if (tab_name == None):
            cur = db1.cursor()
            cur.execute("show tables")
            for row in cur.fetchall():
                self.syn_tab(db1,source_dbname,db2,targe_dbname,row[0])
            cur.close()
        else:
            self.syn_tab(db1,source_dbname,db2,targe_dbname,db_tbname)
        
        db1.close()
        db2.close()

    def syn_tab(self,db1,db1_name,db2,db2_name,tab_name):
        listfld = "COLUMN_NAME,COLUMN_DEFAULT,IS_NULLABLE,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,CHARACTER_OCTET_LENGTH,NUMERIC_PRECISION,NUMERIC_SCALE,DATETIME_PRECISION,COLUMN_TYPE,COLUMN_COMMENT".split(',')
        dctfld = {}
        idx = 0
        for k in listfld:
            dctfld[k] = idx
            idx = idx + 1
        #select * from information_schema.COLUMNS where TABLE_NAME='obj_product_evaluation_9'
        sql1 = "select COLUMN_NAME,COLUMN_DEFAULT,IS_NULLABLE,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,CHARACTER_OCTET_LENGTH,NUMERIC_PRECISION,NUMERIC_SCALE,NULL,COLUMN_TYPE,COLUMN_COMMENT from information_schema.COLUMNS where TABLE_NAME='%s' and TABLE_SCHEMA='%s'" %(tab_name,db1_name)
        sql2 = "select COLUMN_NAME,COLUMN_DEFAULT,IS_NULLABLE,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,CHARACTER_OCTET_LENGTH,NUMERIC_PRECISION,NUMERIC_SCALE,NULL,COLUMN_TYPE,COLUMN_COMMENT from information_schema.COLUMNS where TABLE_NAME='%s' and TABLE_SCHEMA='%s'" %(tab_name,db2_name)
        #
        logger.debug(sql1)
        cur1 = db1.cursor()
        cur1.execute(sql1)
        dct1 = collections.OrderedDict()
        for row in cur1.fetchall():
            dct1[row[0]] = row
        
        cur2 = db2.cursor()
        dct2 = collections.OrderedDict()
        #先判定表释放存在
        cur2.execute("select count(*) from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='%s' and TABLE_NAME='%s'" %(db2_name,tab_name))
        t = cur2.fetchone() 
        if (t[0] == 0):
            cur1.execute("SHOW CREATE TABLE %s" %(tab_name))
            t = cur1.fetchone()
            logger.debug("create table {0}".format(tab_name)) 
            cur2.execute(t[1])
        else:
            cur2.execute(sql2)
            for row in cur2.fetchall():
                dct2[row[0]] = row

            for k,val1 in dct1.items():
                if (dct2.has_key(k) == False):#目标表没有对应字段要添加新字段
                    #"alter table user add COLUMN new1 VARCHAR(20) DEFAULT NULL COMMENT '评价id'"
                    default_val = ""
                    if (val1[dctfld['IS_NULLABLE']] == 'NO'):#是否允许为空
                        default_val = "NOT NULL"
                    else:
                        if (val1[dctfld['COLUMN_DEFAULT']] == None):
                            default_val = "DEFAULT NULL"
                        else:
                            if (val1[dctfld['DATA_TYPE']].find('int') >= 0 or val1[dctfld['DATA_TYPE']].find('real') >= 0 or val1[dctfld['DATA_TYPE']].find('float') >= 0 or val1[dctfld['DATA_TYPE']].find('double') >= 0 or val1[dctfld['DATA_TYPE']].find('decimal') >= 0 or val1[dctfld['DATA_TYPE']].find('numeric') >= 0):
                                default_val = "DEFAULT " + val1[dctfld['COLUMN_DEFAULT']]
                            else:
                                default_val = "DEFAULT '" + val1[dctfld['COLUMN_DEFAULT']] + "'"

                    sql1 = "ALTER TABLE %s ADD COLUMN %s %s %s COMMENT \"%s\"" %(tab_name,k,val1[dctfld['COLUMN_TYPE']],default_val,val1[dctfld['COLUMN_COMMENT']])
                    logger.debug(sql1)
                    cur2.execute(sql1)
                else:#有相同字段再进行字段属性比较
                    val2 = dct2[k]
                    flag = False
                    for i in range(1,len(listfld)) :
                        if (val1[dctfld[listfld[i]]] <> val2[dctfld[listfld[i]]]):
                            flag = True
                    if flag == True:#其中有字段不一样
                        #alter table user MODIFY new1 VARCHAR(10); 
                        default_val = ""
                        if (val1[dctfld['IS_NULLABLE']] == 'NO'):#是否允许为空
                            default_val = "NOT NULL"
                        else:
                            if (val1[dctfld['COLUMN_DEFAULT']] == None):
                                default_val = "DEFAULT NULL"
                            else:
                                if (val1[dctfld['DATA_TYPE']].find('int') >= 0 or val1[dctfld['DATA_TYPE']].find('real') >= 0 or val1[dctfld['DATA_TYPE']].find('float') >= 0 or val1[dctfld['DATA_TYPE']].find('double') >= 0 or val1[dctfld['DATA_TYPE']].find('decimal') >= 0 or val1[dctfld['DATA_TYPE']].find('numeric') >= 0):
                                    default_val = "DEFAULT " + val1[dctfld['COLUMN_DEFAULT']]
                                else:
                                    default_val = "DEFAULT '" + val1[dctfld['COLUMN_DEFAULT']] + "'"
                        sql1 = "ALTER TABLE %s MODIFY %s %s %s COMMENT \"%s\"" %(tab_name,k,val1[dctfld['COLUMN_TYPE']],default_val,val1[dctfld['COLUMN_COMMENT']])
                        logger.debug(sql1)
                        cur2.execute(sql1)
        #同步索引
        #Table                    | Non_unique | Key_name         | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment
        #obj_product_evaluation_0 |          0 | PRIMARY          |            1 | id          | A         |           3 |     NULL | NULL   |      | BTREE      |         |               
        cur1.execute("SHOW INDEX FROM %s" %(tab_name))
        dct1 = collections.OrderedDict()
        for row in cur1.fetchall():
            if (dct1.has_key(row[2]) == False):
                dct1[row[2]] = {'Non_unique' : row[1],'Column_name' : ["`" + row[4] + "`"]}
            else:
                dct1[row[2]]["Column_name"].append("`" + row[4] + "`") 
        
        cur2.execute("SHOW INDEX FROM %s" %(tab_name))
        dct2 = collections.OrderedDict()
        for row in cur2.fetchall():
            if (dct2.has_key(row[2]) == False):
                dct2[row[2]] = {'Non_unique' : row[1],'Seq_in_index' : row[3],'Column_name':["`" + row[4] + "`"]}
            else:
                dct2[row[2]]["Column_name"].append("`" + row[4] + "`")
        
        for k,val1 in dct1.items():
            if (dct2.has_key(k) == False):#目标表没有对应字段要添加新索引
                logger.debug("{0},{1},{2}".format(tab_name,k,val1))
                sql = ""
                sql1 = ""
                if (k == 'PRIMARY'):
                    sql1 = "ALTER TABLE %s ADD PRIMARY KEY (%s)" %(tab_name,','.join(val1['Column_name']))
                elif (val1['Non_unique'] == 0):
                    sql1 = "ALTER TABLE %s ADD UNIQUE %s (%s)" %(tab_name,k,','.join(val1['Column_name']))
                else:
                    sql1 = "ALTER TABLE %s ADD INDEX %s (%s)" %(tab_name,k,','.join(val1['Column_name']))
                if (len(sql1) > 0):
                    logger.debug(sql1)
                    cur2.execute(sql1)
            else:
                val2 = dct2[k]
                #print tab_name,k,val1
                cj = [v for v in val1['Column_name'] if v not in val2['Column_name']]
                if (val1['Non_unique'] <> val2['Non_unique'] or len(cj) > 0):
                    logger.debug("{0},{1},{2}".format(tab_name,k,val1))
                    sql = ""
                    sql1 = ""
                    if (k == 'PRIMARY'):
                        sql = "ALTER TABLE %s DROP PRIMARY KEY" %(tab_name)
                        sql1 = "ALTER TABLE %s ADD PRIMARY KEY (%s)" %(tab_name,','.join(val1['Column_name']))
                    elif (val1['Non_unique'] == 0):
                        sql = "ALTER TABLE %s DROP UNIQUE %s" %(tab_name,k)
                        sql1 = "ALTER TABLE %s ADD UNIQUE %s (%s)" %(tab_name,k,','.join(val1['Column_name']))
                    else:
                        sql = "ALTER TABLE %s DROP INDEX %s" %(tab_name,k)
                        sql1 = "ALTER TABLE %s ADD INDEX %s (%s)" %(tab_name,k,','.join(val1['Column_name']))
                    if (len(sql) > 0):
                        cur2.execute(sql)
                    if (len(sql1) > 0):
                        cur2.execute(sql1)

        cur1.close()
        cur2.close()


    def get_prepare(self,db,tab_name):
        cur = db.cursor()
        cur.execute("select * from %s limit 1" %(tab_name))
        list_fields = cur.description
        sql = ''
        val = ''
        for k in list_fields:
            if (len(sql) > 0):
                sql = sql + ","
                val = val + ","
            sql = sql + "`" + k[0] + "`"
            val = val + "?"
        print(sql)
        print("insert into %s(%s) values(%s)" %(tab_name,sql,val))
        cur.close()

# logger.setLevel(logging.INFO)
# h = syntab('user1:pass1@127.0.0.1:3306','user3:pass3@127.0.0.2:3307')
# h.syn('source_db1','test_db2',None)
