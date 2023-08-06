# -*- coding: utf-8 -*-

import pymysql
import pandas as pd

class Mysql(object):

	def __init__(self,host,user,password,tbname):
		self.host = host
		self.user = user
		self.password = password
		self.tbname = tbname
		self.connectsql()
		
	def connectsql(self):
		self.conn=pymysql.connect(host=self.host,user=self.user,password=self.password,database='%s' % self.tbname)
		self.cur=self.conn.cursor()
	
	def runsql(self,sql):
		self.cur.execute(sql)
		self.conn.commit()
		
	def fetchsql(self,sql):
		self.cur.execute(sql)
		result = self.cur.fetchall()
		return result
		
	def pdsql(self,sql):
		df = pd.read_sql(sql,self.conn)
		return df
		
	def close():
		self.cur.close()
		self.conn.close()
if __name__ == '__main__':
	host='localhost'
	user='root'
	password='zhang7186169'
	tbname='mysql'
	Mysql(host,user,password,tbname)