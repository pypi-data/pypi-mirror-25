import json
from geojson_utils import point_in_polygon
from zqy.usually import zqy

def disall(path):
    #求每个点的累加距离
    if len(path) > 1:
        dis = 0
        ldis = [0]
        l1 = path[:-1]
        l2 = path[1:]
        l = list(zip(l1,l2))
        for i in l:
            a,b,c,d = i[0][0], i[0][1], i[1][0], i[1][1]
            dis = dis + zqy.distance(a,b,c,d)
            ldis.append(dis)

        out1 = [x[0] for x in path]
        out2 = [x[1] for x in path]
        out3 = [round((x / max(ldis)),2) for x in ldis]
        pathout = list(zip(out1,out2,out3))
        return pathout
    else:
        return [(path[0][0], path[0][1], 1)]

def caldis(path1,path2):
    d = 0
    dis1 = [x[-1] for x in path1]
    dis2 = [x[-1] for x in path2]

    n = 0
    for index1 in range(len(dis1)):
        n += 1
        l1 = [dis1[index1]] * len(dis2)
        l2 = dis2
        l = list(zip(l1, l2))
        ldelta = [abs(x[0] - x[1]) for x in l]
        index2 = ldelta.index(min(ldelta))
        d = d + zqy.distance(path1[index1][0], path1[index1][1], path2[index2][0], path2[index2][1])
    d = round((d / n),2)
    return d

def pathdis(path1, path2):
    #求两条轨迹的距离
    if len(path1) < len(path2):
        path1, path2 = path2, path1
    path1accu = disall(path1)
    path2accu = disall(path2)
    d = caldis(path1accu, path2accu)
    return d

class Zqypathloc(object):

    def __init__(self, path):
        self.path = path

    def disod(self):
        #返回OD直线距离
        x1, y1 = self.path[0]
        x2, y2 = self.path[-1]
        disod = zqy.distance(x1, y1, x2, y2)
        return disod

    def angleeach(self):
        #返回每次转弯的角度
        l = list(zip(self.path[:-1], self.path[1:]))
        langle = [zqy.angle(x[0][0], x[0][1], x[1][0], x[1][1]) for x in l]
        return langle

    def perline(self):
        #返回轨迹非直线系数
        disod = self.disod()
        disall = self.disall()
        out = round((disall * disall / disod), 3)
        return out

    def nodenum(self):
        #返回路径节点个数
        return len(self.path)

    def disall(self):
        #返回路径总距离
        l = list(zip(self.path[:-1], self.path[1:]))
        ldis = [zqy.distance(x[0][0], x[0][1], x[1][0], x[1][1]) for x in l]
        return sum(ldis)

    def turnnum(self, anglemax=45):
        #返回转弯次数
        langle = self.angleeach()
        langle = [x for x in langle if x >= anglemax]
        out = len(langle)
        return out

    def nearbypoint(self, lpoint, dis):
        #返回轨迹周边的点的集合
        #先求线偏移角度
        langle = self.angleeach()
        langle1, langle2 = [], []
        for i in langle:
            if i <= 180:
                j1 = i + 270
                j2 = i + 90
            else:
                j1 = i + 90
                j2 = i + 270
            if j1 >= 360:
                j1 = j1 - 360
            if j2 >= 360:
                j2 = j2 - 360
            langle1.append(j1)
            langle2.append(j2)
        lmiddle1 = [min([x[0], x[1]]) + abs(x[0] - x[1]) / 2 for x in list(zip(langle1[:-1], langle1[1:]))]
        lmiddle2 = [min([x[0], x[1]]) + abs(x[0] - x[1]) / 2 for x in list(zip(langle2[:-1], langle2[1:]))]
        langleall = [langle1[0]] + lmiddle1 + [langle1[-1]] + [langle2[-1]] + lmiddle2 + [langle2[0]]

        path1 = self.path
        path2 = path1.copy()
        path2.sort(reverse=True)
        lpathnodeall = path1 + path2
        lnodeangle = zip(lpathnodeall, langleall)

        #偏移成线成为缓冲区边界
        linebuffer = []
        for i in lnodeangle:
            p, myangle = i
            d = zqy.finddestination(p, myangle, dis)
            linebuffer.append(d)

        #建立面要素，判断点集中的点是否在面内
        lout = []
        linebuffer = ['[' + str(x[0]) + ', ' + str(x[1]) + ']' for x in linebuffer]
        sinebuffer = ', '.join(linebuffer)
        box_str = '{"type": "Polygon","coordinates": [[ %s ]]}' % sinebuffer
        box = json.loads(box_str)
        for p in lpoint:
            mystr = '{"type": "Point", "coordinates": [%s, %s]}' % (p[0], p[1])
            myp = json.loads(mystr)
            if point_in_polygon(myp, box):
                lout.append(p)
        return lout






if __name__ == '__main__':
    from pylab import *
    path = [(1,1),(2,2),(3,5)]
    a = Zqypathloc(path)
    lpoint = [(1,1.2), (1, 3)]
    l = a.nearbypoint(lpoint, 1)
    print(l)
