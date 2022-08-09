import xlrd
from Code.Ordernum import NUM
import csv

def GetData():
    filepath = r"C:\Users\Administrator\Desktop\豆瓣TOP250.xls"
    file = xlrd.open_workbook(filepath)
    sheet = file.sheets()[0]
    '''
    # sheet = table.sheet_by_index(0) 通过下标读取表格
    # sheet = table.sheet_by_name('新增账号') 通过名称读取表格
    '''

    rows = sheet.nrows
    cols = sheet.ncols

    x = []
    for i in range(1, rows):
        line = sheet.row_values(i)
        line[NUM.ACTOR] = line[NUM.ACTOR].split(" / ")
        line[NUM.DIRECTOR] = line[NUM.DIRECTOR].split(" / ")
        line[NUM.TYPE] = line[NUM.TYPE].split(" / ")
        line[NUM.WRITER] = line[NUM.WRITER].split(" / ")
        x.append(line)

    y = []
    for i in range(cols):
        line = sheet.col_values(i)
        del line[0]
        if i == NUM.ACTOR or i == NUM.DIRECTOR or i == NUM.TYPE or i == NUM.WRITER:
            line = list(map(lambda x: x.split(" / "), line))
        y.append(line)
    return x, y


def GetID(data):
    # movie,director,actor,type
    id_index = 0
    ids = {}
    id_name = {}
    col_index = [NUM.DIRECTOR, NUM.ACTOR, NUM.TYPE]
    for movie in data[NUM.MOVIE]:
        id_name[id_index] = movie
        if movie not in ids:
            ids[movie] = [id_index]
        else:
            ids[movie].append(id_index)
        id_index += 1

    for i in range(3):
        id_index = 10000 * (i + 1)
        for nodes in data[col_index[i]]:  # 一部电影中的全部导演/演员/类型
            for node in nodes:  # 一部电影中的单个导演/演员/类型
                if node not in ids:
                    id_name[id_index] = node
                    ids[node] = id_index
                    id_index += 1
    return ids, id_name


def search_recommendations(link, id_name, name_id, name):
    # 电影不存在
    if name not in name_id:
        print("not in data")
        return []
    # 电影存在
    '''
    ans:
        {movie_id:{id,id,id}}
    '''
    ans = {}
    id = name_id[name]
    for node2 in link[id]:
        for node3 in link[node2]:
            if node3 in ans:
                ans[node3].append(node2)
            else:
                ans[node3] = [node2]
    '''
    first10:
        [ [movie,[relation,relation,relation]],[……] ]
    '''
    first10 = []
    for i in range(min(len(ans), 11)):
        num = -1
        max_key = -1
        for key, value in ans.items():
            if len(value) > num:
                num = len(value)
                max_key = key
        first10.append([max_key, ans[max_key]])
        del ans[max_key]
    # 删除自己
    del first10[0]

    ans = []
    relation_type = {1: "类型", 2: "导演", 3: "演员"}
    for each in first10:
        '''each = [movie,[relation1,relation2,……]]'''
        movie = [id_name[each[0]]]
        for every in each[1]:
            movie.append(id_name[every])
            movie.append(relation_type[every // 10000])
        ans.append(movie)
    '''
    ans:
        [  [movie,[relaiton,relaitontype],[relaiton,relaitontype],[……]]  ]
    '''
    return ans


def GetLink3():
    id_name = {}
    name_id = {}
    link = {}
    x, y = GetData()
    id_movie, id_type, id_direct, id_actor = 0, 10000, 20000, 30000

    for line in x:
        movie = line[NUM.MOVIE]
        type = line[NUM.TYPE]
        direct = line[NUM.DIRECTOR]
        actor = line[NUM.ACTOR]

        # movie
        id_movie += 1
        id_name[id_movie] = movie
        name_id[movie] = id_movie
        link[id_movie] = []

        for each in type:
            if each not in name_id:
                id_type += 1
                name_id[each] = id_type
                id_name[id_type] = each
                link[id_type] = [id_movie]
                link[id_movie].append(id_type)
            else:
                link[name_id[each]].append(id_movie)
                link[id_movie].append(name_id[each])

        for each in direct:
            if each not in name_id:
                id_direct += 1
                name_id[each] = id_direct
                id_name[id_direct] = each
                link[id_direct] = [id_movie]
                link[id_movie].append(id_direct)
            else:
                link[name_id[each]].append(id_movie)
                link[id_movie].append(name_id[each])
        for each in actor:
            if each not in name_id:
                id_actor += 1
                name_id[each] = id_actor
                id_name[id_actor] = each
                link[id_actor] = [id_movie]
                link[id_movie].append(id_actor)
            else:
                link[name_id[each]].append(id_movie)
                link[id_movie].append(name_id[each])

    return link, id_name, name_id


def LoadLink():
    x, y = GetData()
    link, id_name, name_id = GetLink3()
    path = r"C:\Users\Administrator\Desktop\recommendation.csv"
    file = open(path, "w", encoding="utf-8", newline='')
    csv.writer(file).writerow(["名字", "关系", "关系类型", "关系", "关系类型", "关系", "关系类型", "关系", "关系类型"])
    for movie in y[0]:
        path = search_recommendations(link, id_name, name_id, movie)
        for i in range(min(10, len(path))):
            path[i].insert(0, movie)
            csv.writer(file).writerow(path[i])