import csv
from Code.Ordernum import NUM


class NODE:
    def __init__(self, id, name, att):
        self.id = id  # 节点的ID
        self.name = name  # 节点的名称
        self.att = att  # 节点的标签


class EDGE:
    def __init__(self, node1, node2, relation):
        self.NodeStart = node1  # 边的起始节点
        self.NodeEnd = node2  # 边的结束节点
        self.att = relation  # 边的标签（节点间的关系）


def loadnode(id):
    # 最终还是选择用id作为node，因为有重名的电影。
    # path = r"C:\Users\Administrator\Desktop\node.csv"
    # file = open(path, "w", encoding="utf-8", newline='')
    # csv.writer(file).writerow(["类型", "ID", "名称", "标签"])

    att = ["电影", "导演", "演员", "类型"]
    nodes = []
    for key, value in id.items():
        if isinstance(value, list):
            for va in value:
                name = att[va // 10000]
                # line = [name, va, key, name]
                node = NODE(va, key, name)
                nodes.append(node)
                # nodes.append([name, va, key])
                # csv.writer(file).writerow(line)
        else:
            name = att[value // 10000]
            node = NODE(value, key, name)
            nodes.append(node)
            # line = [name, value, key, name]
            # nodes.append([name, value, key])
            # csv.writer(file).writerow(line)
    # file.close()
    return nodes


def loadedge(x, ids):
    # path = r"C:\Users\Administrator\Desktop\movie_relation.csv"
    # file = open(path, "w", encoding="utf-8", newline='')
    # csv.writer(file).writerow(["名字", "名字", "关系"])
    edges = []
    i = -1
    for row in x:
        i += 1
        movie = row[NUM.MOVIE]
        for di in row[NUM.DIRECTOR]:
            # line = [di, movie, "导演"]
            # id_line = [ids[di], i, "导演"]
            edge = EDGE(ids[di],i,"导演")
            edges.append(edge)
            # edges.append(id_line)
            # csv.writer(file).writerow(line)
        for ty in row[NUM.TYPE]:
            edge = EDGE(i, ids[ty], "属于")
            edges.append(edge)
            # line = [movie, ty, "属于"]
            # id_line = [i, ids[ty], "属于"]
            # edges.append(id_line)
            # csv.writer(file).writerow(line)
        for ac in row[NUM.ACTOR]:
            edge = EDGE(ids[ac], i, "出演")
            edges.append(edge)
            # line = [ac, movie, "出演"]
            # id_line = [ids[ac], i, "出演"]
            # edges.append(id_line)
            # csv.writer(file).writerow(line)
        for di in row[NUM.DIRECTOR]:
            for ac in row[NUM.ACTOR]:
                if di == ac:
                    continue
                edge = EDGE(ids[di], ids[ac], "合作")
                # id_line = [ids[di], ids[ac], "合作"]
                if edge in edges:
                    continue
                # line = [di, ac, "合作"]
                edges.append(edge)
                # csv.writer(file).writerow(line)
    # file.close()
    return edges
