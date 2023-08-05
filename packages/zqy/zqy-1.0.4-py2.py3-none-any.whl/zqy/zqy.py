# -*- coding: utf-8 -*-

from scipy import spatial
import pandas as pd
import types,os,datetime,time,random,bisect,utm,pymysql
from math import radians, cos, sin, asin, sqrt, atan, pi
import numpy as np

def breakdf(df,part):
	#将df按人数成多少份，输入的df必须用msid和day两个字段
	nummsid = len(df.groupby(['msid']))
	x = nummsid / part
	y = 0
	l = [0]
	for i in range(part):
		if i != part - 1:
			y = y + x
			l.append(y)
		else:
			l.append(nummsid - 1)
	l_msid = df['msid'].drop_duplicates().tolist()
	l_df = []
	for i in range(len(l)):
		if i + 1 < len(l):
			index1 = l[i]
			index2 = l[i + 1]
			l_msidone = l_msid[index1:index2]
			dfone = pd.DataFrame({'msid':l_msidone},index = None)
			dfpart = pd.merge(df,dfone,on = 'msid')
			l_df.append(dfpart)
	return l_df

class Bar(object):
	#每隔1%显示一次进度条
	def __init__(self,all,breaking = 1):
		self.all = all
		self.now = 0
		self.one = float(all) * 0.01 * breaking
		self.part = self.one
		self.time1 = timenow()
		self.timesum = 0
	
	def cal(self):
		self.now += 1
		if self.now >= self.part:
			time2 = timenow()
			self.timesum = (str2time(time2) - str2time(self.time1)).seconds / 60.0
			timeall = float(self.timesum * self.all) / float(self.now)
			timeleft = timeall - self.timesum
			if timeleft <= 60:
				printtime = round(timeleft,2)
				printpercent = int(float(self.now) / float(self.all) * 100)
				print('%s:%s%%,timeleft:%smin' % (os.getpid(),printpercent,printtime))
			else:
				timeleft = timeleft / 60.0
				printtime = round(timeleft,2)
				printpercent = int(float(self.now) / float(self.all) * 100)
				print('%s:%s%%,timeleft:%sh' % (os.getpid(),printpercent,printtime))
			self.part = self.part + self.one

def distance(lng1,lat1,lng2,lat2, roundnum=4):
	dis = ((lng1 - lng2) ** 2 + (lat1 - lat2) ** 2) ** 0.5
	dis = round(dis, roundnum)
	return dis
	
def middlepoint(p1, p2):
	x = (p1[0] + p2[0]) / 2
	y = (p1[1] + p2[1]) / 2
	return (x, y)

def str2time(s): 
	#字符串转时间格式
	s = str(s)
	return datetime.datetime.strptime(s,'%Y%m%d%H%M%S')
 
def time2str(time): 
	#时间格式转字符串
    return time.strftime('%Y%m%d%H%M%S')
	
def time2int(time): 
	#时间格式转字符串   
    return int(time.strftime('%Y%m%d%H%M%S'))

def utm2wgs(lng,lat):
    lat2,lng2 = utm.to_latlon(lng,lat,51,'R')
    return lng2,lat2
	
def wgs2utm(lng,lat):
    lng2,lat2,a,b = utm.from_latlon(lat,lng)
    return lng2,lat2

def tree(tree,point,dis):
	#输入点集、点、距离，返回距离内的点集
    point = (point[0],point[1])
    return tree.query_ball_point(point,dis)
	
def buildtree(df,lngname='lng',latname='lat'):
	'''
	输入一个df，有lng，lat两个字段
	返回一个kdtree
	'''
	llng = df[lngname].tolist()
	llat = df[latname].tolist()
	lpoint = list(zip(llng,llat))
	tree = spatial.KDTree(lpoint)
	return tree
	
def df2list(df, xname='lng', yname='lat'):
	x, y = df[xname].tolist(), df[yname].tolist()
	l = list(zip(x,y))
	return l
	
def listzip(l):
	return list(zip(l[:-1], l[1:]))
	
def angle(x_point_s,y_point_s,x_point_e,y_point_e):
    angle=0
    y_se= y_point_e-y_point_s;
    x_se= x_point_e-x_point_s;
    if x_se==0 and y_se>0:
        angle = 360
    if x_se==0 and y_se<0:
        angle = 180
    if y_se==0 and x_se>0:
        angle = 90
    if y_se==0 and x_se<0:
        angle = 270
    if x_se>0 and y_se>0:
       angle = atan(x_se/y_se)*180/np.pi
    elif x_se<0 and y_se>0:
       angle = 360 + atan(x_se/y_se)*180/np.pi
    elif x_se<0 and y_se<0:
       angle = 180 + atan(x_se/y_se)*180/np.pi
    elif x_se>0 and y_se<0:
       angle = 180 + atan(x_se/y_se)*180/np.pi
    return angle
	
class Dftree(object):
	def __init__(self, df, xname='lng', yname='lat'):
		self.df = df
		self.lngname = xname
		self.latname = yname
		self.lnode = self.buildnode()
		self.tree = self.buildtree()
	
	def buildnode(self):
		llng = self.df[self.lngname].tolist()
		llat = self.df[self.latname].tolist()
		lpoint = list(zip(llng,llat))
		return lpoint
		
	def buildtree(self):
		tree = spatial.KDTree(self.lnode)
		return tree
		
	def nearestnode(self, p, showlocation=False,showdis=False, showindex=False, roundnum=4):
		ldfindex = list(self.df.index)
		dis,index = self.tree.query(np.array(p))
		indexout = ldfindex[index]
		lng = self.df.iloc[index][self.lngname]
		lat = self.df.iloc[index][self.latname]
		lng, lat = [round(x,roundnum) for x in [lng, lat]]
		
		linput = [showlocation, showdis, showindex]
		lout = [(lng, lat), dis, indexout]
		lout2 = []
		for i in range(3):
			if linput[i]:
				lout2.append(lout[i])
		return lout2
		
	def nearbynode(self, p, dis, showlocation=False, showindex=False,roundnum=None):
		lindex = self.tree.query_ball_point(p, dis)
		ldfindex = list(self.df.index)
		llng = [self.df.iloc[x][self.lngname] for x in lindex]
		llat = [self.df.iloc[x][self.latname] for x in lindex]
		lindexout = [ldfindex[x] for x in lindex]
		if roundnum != None:
			llng = [round(x,roundnum) for x in llng]
			llat = [round(x,roundnum) for x in llat]
		llocation = list(zip(llng, llat))
		
		linput = [showlocation, showindex]
		lout = [llocation, lindexout]
		lout2 = []
		for i in range(2):
			if linput[i]:
				lout2.append(lout[i])
		return lout2
		
def quadrantnum(po, p):
	#输入基准点和点，返回该点所在的象限
	lng, lat = po
	lngp, latp = p
	if lngp >= lng and latp >= lat:
		return 1
	if lngp >= lng and latp <= lat:
		return 2
	if lngp <= lng and latp <= lat:
		return 3
	if lngp <= lng and latp >= lat:
		return 4
		
def float2str(p):
	return (str(p[0]), str(p[1]))

def str2float(p):
	return (float(p[0]), float(p[1]))
	
def dict2dfaccu(dic,name = ['key','weight','weightaccu']):
	#将字典的key和value分别作为两列创建df,后面加一列累积值。
	#accu为是否累加
	key = list(dic.keys())
	weight = list(dic.values())
	weight1 = []
	weight2 = []
	weightsum = 0
	for i in weight:
		weightsum = weightsum + i
		weight2.append(weightsum)
		weight1.append(i)
	return pd.DataFrame({name[0]:key,name[1]:weight1,name[2]:weight2},index = None)
	
def dict2df(dic,name = ['key','weight']):
	#将字典的key和value分别作为两列创建df
	key = list(dic.keys())
	weight = list(dic.values())
	return pd.DataFrame({name[0]:key,name[1]:weight},index = None)
	
		
def putindl(dicl,x):
	#如果某值不在列表里，将该值放进去
	#如果某值在列表里，不将该值放进去
	#如果某值不在字典里，将该值作为key放进去，value为1
	#如果某值在字典里，value加一
    if x not in dicl:
        if type(dicl) == types.DictType:
            dicl[x] = 1
        else:
            dicl.append(x)
    else:
        if type(dicl) == types.DictType:
            dicl[x] += 1

def getday(day):
    day = int(day)
    return int((day % 100000000)) / 1000000
def geth(h):
    h = int(h)
    return int((h % 1000000)) / 10000
	
def acculist(l):
    #将列表中的每一项累加，生成新的列表
    l_sum = []
    sumweight = 0
    for a in l:
        sumweight += a
        l_sum.append(sumweight)
    return l_sum
	
def timenow():
	#返回当前时间，字符串格式
	return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

def weight_choice(l_weight):
	#输入累加后的列表，列表中的值作为权重，根据权重随机选择一项，但会
	"""
	:param weight: list对应的权重序列
	:return:选取的值在原列表里的索引
	"""
	weightmax = max(l_weight)
	t = random.randint(0, (weightmax - 1))
	return bisect.bisect_right(l_weight, t)
	
def datetimeornot(time):
	'''输入一个时间，判断是否为时间格式，返回时间格式的时间'''
	if isinstance(time,datetime.datetime) == True:
		return time
	else:
		return str2time(time)
		
def timelength(time1,time2):
	'''输入两个int时间，返回时长单位为秒'''
	time1 = datetimeornot(time1)
	time2 = datetimeornot(time2)
	if time1 == time2:
		return 0
	else:
		delta = (time2 - time1).seconds
		return delta
		
	
def insertdatetime(df,loc,timename = 'tstamp',newname = 'datetime'):
	dic_time = {}
	key = 0
	for index,row in df.iterrows():
		time = str2time(row[timename])
		dic_time[key] = time
		key += 1
	se_time = pd.Series(dic_time)
	df.insert(loc,newname,se_time)
	return df


def clearpath(path,columns = None):
	'''
	清空之前存在的文件
	如果不存在文件创建之
	'''
	o = open(path,'w')
	if columns != None:
		oo = ''
		for i in columns:
			oo = oo + i + ','
		oo = oo.strip(',')
		oo = oo + '\n'
		o.write(oo)
	o.close()

def sqlinsert(df,tablename):
	'''输入一个df，返回插入此df的sql原生语言'''
	oo = ''
	for index,row in df.iterrows():
		o = '('
		for i in range(len(row)):
			ii = row[i]
			if i == 0:
				o = o + '\'%s\'' % ii+ ','
			else:
				o = o + '%s' % ii + ','
		o = o.strip(',')
		o = o + ')'
		oo = oo + o + ','
	oo = oo.strip(',')
	sql = 'insert into %s values %s' % (tablename,oo)
	return sql

def runsql(sql,conn,cur):
	cur.execute(sql)
	conn.commit()

def connectsql(tbname):
	conn=pymysql.connect(host='localhost',user='root',password='zhang7186169',database='%s' % tbname)
	cur=conn.cursor()
	return conn,cur
	
def breakdfeach(df,each):
	l1 = range(0,len(df),each)
	l2 = range(each,(len(df) + each),each)
	return list(df.iloc[x:y] for x,y in zip(l1,l2))
	

def breakdftime(df,time):
	'''切分时间点，输出切分的index集合'''
	l_breakindex = [0]
	for i in range(len(df)):
		if (i + 1) < len(df):
			time2 = str2time(df.iloc[i + 1]['tstamp'])
			time1 = str2time(df.iloc[i]['tstamp'])
			time_delta = (time2 - time1).seconds
			if time_delta > time:
				l_breakindex.append(i + 1)
				
	l_breakindex.append(len(df))
	l1 = l_breakindex[:-1]
	l2 = l_breakindex[1:]
	
	return list(df.iloc[x:y] for x,y in zip(l1,l2))

def writecolumns(path,df):
	'''
	输入空文件路径，一个df
	将df的列名写入文件
	最后关闭文件
	'''
	o = open(path,'w')
	oo = ''
	for i in df.columns:
		oo = oo + '%s' % i + ','
	oo = oo.strip(',')
	oo = oo + '\n'
	o.write(oo)
	o.close()

def centerpoint(dfpoint,lngname = 'lng',latname = 'lat'):
	'''
	输入一个df
	包括lng，lat两个字段
	求一组点集的平均中心
	'''
	lngavg = float(sum(dfpoint[lngname])) / float(len(dfpoint))
	latavg = float(sum(dfpoint[latname])) / float(len(dfpoint))
	return (lngavg,latavg)
	
def centertime(setime,order = False):
	'''
	输入一个含有时间字段的se，可以是时间格式，也可以不是
	返回中间时刻，int
	'''
	setime = setime.tolist()
	if order == True:
		se.sort_values()
	time1 = datetimeornot(setime[0])
	time2 = datetimeornot(setime[-1])
	timedelta = timelength(time1,time2)
	timemiddle = time1 + datetime.timedelta(seconds = timedelta / 2)
	return time2int(timemiddle)
	
def gaodekey():
	#随机返回一个高德key
	key1 = 'bcb4190e817908e737edafed0c8742b6'
	key2 = "7ca6c1505b1c211ebe0aa42412982b24"
	key3 = "8ccb99c2fa7499b367a1b7e85509b1ac"
	key4 = "a1ad3a7fbdaf3de9a4e421c35b0c09c3"
	list_key = [key1,key2,key3,key4]
	return list_key[random.randint(0,3)]
	
def finddestination(p, angle, dis):
	#输入角度，距离，起点坐标，返回终点坐标
	angle = angle * pi / 180
	deltax = dis * sin(angle)
	deltay = dis * cos(angle)
	x, y = p
	out = ((x + deltax), (y + deltay))
	return out
  
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """  
    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000
	
def combinelist(l):
	lindex = list(range(len(l)))
	dic = {key:value for (key, value) in zip(lindex, l)}
	dic = {key:value for (value, key) in dic.items()}
	dic = {key:value for (value, key) in dic.items()}
	lout =[dic[key] for key in sorted(dic.keys())]
	return lout
	
def findmaxormin(l1, l2, maxormin='max'):
	#两个列表，根据列表1找到最大或最小的项，返回与之位置对应的列表2中的元素
	if maxormin == 'max':
		x = max(l1)
	if maxormin == 'min':
		x = min(l1)
	index = l1.index(x)
	return l2[index]
	
if __name__ == '__main__':
	p = r"E:\20170329_抽稀\加密轨迹加小时加街道前3000行.csv"
	#df = pd.read_csv(p)
	#print(breakdftime(df,120))
	l = ['a','a','b','b','c','d','f','f','m','n']
	print(combinelist(l))