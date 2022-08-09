# -*- coding: utf-8 -*-

from GetData import GetData, GetID
from Load import loadnode, loadedge
from BuildG import buildG
from Search import search




# --------------------------------------------------------------------------------------------------------
'''
x:          以每部电影为单位
                [[片名，年份，人数，[导演]，[编剧]，[主演]，[类型]，国家，语言，市场],……]
y:          以每个类型为单位
                [[片名]，[年份]，……]
node:       以每个节点为单位
                [[节点类型，id，节点名字],[],[]……]
edge:       [[id，id，关系],[id，id，关系],……]
id:         {电影：[1,2,3],电影：[4],演员：10005，导演：200006}
'''
# --------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    x, y = GetData()
    name_id, id_name = GetID(y)
    node = loadnode(name_id)
    edge = loadedge(x, name_id)
    G, GG = buildG(node, edge)
    name = 'input'
    search(G, GG, id_name, name)
