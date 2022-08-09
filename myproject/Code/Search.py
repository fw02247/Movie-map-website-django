from Code.GetData import GetData, GetID
from Code.Load import loadnode, loadedge
from Code.DrawG import draw
from Code.BuildG import buildWG,buildG
from Code.Ordernum import NUM
from Code.Load import NODE,EDGE
import csv
from django.shortcuts import render

def search(G, GG, id_name, text):
    '''
    nodes  [节点类型，id，节点名字]
    edges  [id，id，关系]
    '''

    nodes, edges = [], []
    type_num = ["电影", "导演", "演员", "类型"]

    for id, name in id_name.items():
        if name == text:
            type = type_num[id // 10000]
            node = NODE(id,name,type)
            nodes.append(node)
            for id2, dict in G[id].items():
                type = type_num[id2 // 10000]
                no = NODE(id2,id_name[id2],type)
                nodes.append(no)
                edge = EDGE(id,id2,dict['relationship'])
                edges.append(edge)
            for id2, dict in GG[id].items():
                type = type_num[id2 // 10000]
                node = NODE(id2,id_name[id2],type)
                nodes.append(node)
                edge = EDGE(id2,id,dict['relationship'])
                edges.append(edge)
    return nodes, edges


def search_works(name):
    x, y = GetData()
    name_id, id_name = GetID(y)
    edges = loadedge(x, name_id)

    actor_works = []
    direct_works = []
    if name not in name_id:
        return actor_works, direct_works
    for edge in edges:
        node1, node2, relation = edge.NodeStart,edge.NodeEnd,edge.att
        if node1 == name_id[name]:
            if relation == "导演":
                direct_works.append(id_name[node2])
            elif relation == "出演":
                actor_works.append(id_name[node2])
    return actor_works, direct_works


def search_relations(input1, input2):
    x, y = GetData()
    name_id, id_name = GetID(y)
    nodes = loadnode(name_id)
    edges = loadedge(x, name_id)
    G = buildWG(nodes, edges)

    if input1 not in name_id or input2 not in name_id:
        return []
    print("-----------------------------------------------------")
    inputid1 = name_id[input1]
    inputid2 = name_id[input2]
    if isinstance(inputid1, list):
        inputid1 = inputid1[0]
    if isinstance(inputid2, list):
        inputid2 = inputid2[0]

    path = [[[inputid1, '']]]
    while path:
        list1 = path[0]
        for node1 in list1:
            if node1[0] == inputid2:
                return list1
        node1 = list1[-1][0]
        for id, dict in G[node1].items():
            node2 = [id, dict['relationship']]
            if node2 in list1:
                continue
            list2 = []
            for node in list1:
                list2.append(node)
            list2.append(node2)
            path.append(list2)
        del path[0]
    return []


def search_asks(ask1, ask2, input1):
    ans = []
    x, y = GetData()
    index = {"电影": NUM.MOVIE, "导演": NUM.DIRECTOR, "演员": NUM.ACTOR, "类型": NUM.TYPE}
    askindex = index[ask1]
    ansindex = index[ask2]
    for line in x:
        if isinstance(line[askindex], list) and input1 in line[askindex]:
            ans.append(line[ansindex])
        elif line[askindex] == input1:
            ans.append(line[ansindex])
    return ans


def search_recommendations(name):
    path = r"C:\Users\Administrator\Desktop\recommendation.csv"
    file = open(path, encoding='utf-8')
    is_find = 0
    ans = []
    '''
    ans:
        [ [movie,[relaiton,relaitontype,relaiton,relationtype,...]],  [movie2,……] ]
    '''
    for line in csv.reader(file):
        if line[0] == name:
            del line[0]
            movie = line[0]
            del line[0]
            ans.append([movie, line])
        else:
            if is_find:
                return ans
    return ans


def search_detail(name):
    x,y = GetData()
    for line in x:
        if line[0] == name:
            return line
    return []


def search_contain(request, contain):
    x, y = GetData()
    name_id, id_name = GetID(y)
    node = loadnode(name_id)
    edge = loadedge(x, name_id)
    G, GG = buildG(node, edge)
    nodes, edges = search(G, GG, id_name, contain)
    if nodes:
        flag = 1
        GGG, GGGG = buildG(nodes, edges)
        draw(GGG)
        '''
        pic = draw(GGG)
        # 转为html格式图片
        pic = base64.b64encode(pic).decode()
        pic = "data:image/png;base64," + pic
        '''
        return render(request, 'all.html', locals())
    else:
        flag = 2
        return render(request, 'all.html', locals())

