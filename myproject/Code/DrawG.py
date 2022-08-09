import networkx as nx
from matplotlib import pyplot as plt
from io import BytesIO


def draw(G):
    plt.clf()
    # init
    node_labels = nx.get_node_attributes(G, 'name')
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    node_label2 = nx.get_node_attributes(G, 'att')
    # color
    relation = list(edge_labels.values())
    node_type = list(node_label2.values())
    relation_num = {"导演": 'red', "合作": 'skyblue', "出演": 'orange', "属于": "green"}
    node_num = {"导演": "red", "演员": "skyblue", "电影": "orange", "类型": "green"}
    color_edge = [relation_num[i] for i in relation]
    color_node = [node_num[i] for i in node_type]
    # 画图
    pos = nx.shell_layout(G)
    # 画点
    nx.draw(G, pos, node_color=color_node, edge_color=color_edge, alpha=0.7, node_size=1500, width=0.3)
    # 点的标签
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    # 边的标签
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, alpha=1, bbox=dict(alpha=0))
    '''
    # 转为base64格式图片
    buffer = BytesIO()
    plt.savefig(buffer)
    pic = buffer.getvalue()
    return pic
    '''
    plt.savefig(r"C:\Users\Administrator\Desktop\myproject\myproject\static\pic2\pic.jpg")



'''
    【draw_network_labels】
    G	图。一个网络Graph
    pos	字典。以节点作为键、位置作为值的字典。位置应该是长度为2的序列
    nodelist	列表，可选。只绘制指定的节点(默认为G.nodes())
    node_size	标量或数组。节点的大小(默认值为300)。如果指定了数组，则数组的长度必须与节点列表相同
    node_color	颜色字符串或浮点数数组。节点的颜色。可以是单个颜色格式字符串(默认为’ r ')，也可以是与nodelist相同长度的颜色序列。如果指定了数值，则使用cmap和vmin、vmax参数将它们映射为颜色
    node_shape	字符串。节点的形状。’ so^>v<dph8 ’ 其中之一 (默认= ’ o ')
    alpha	浮点数。节点透明度(默认=1.0)
    cmap	Matplotlib色图。用于映射节点强度的色图(默认=None)
    vmin	浮点数。节点颜色映射缩放的最小值(默认=None)
    vmax	浮点数。节点颜色映射缩放的最大值(默认=None)
    ax	Matplotlib Axes 对象，可选。在指定的Matplotlib轴中绘制图形
    linewidths	[无|标量|序列]。符号边框的线宽(默认=1.0)
    label	[无|字符串]。图例的标签
    【draw】
    pos——布局，参数如下：
        circular_layout：节点在一个圆环上均匀分布
        random_layout：节点随机分布
        shell_layout：节点在同心圆上分布
        spring_layout： 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
        spectral_layout：根据图的拉普拉斯特征向量排列节点

    node_size         
            节点的尺寸大小（默认是300）
    node_color     
            节点的颜色，可以用十六进制颜色码 / 字符串简单标识颜色
    node_shape	
            节点的形状（默认是圆形，用字符串’o’标识）
    alpha	
            透明度（默认是1.0，不透明，0为完全透明）
    width	
            边的宽度（默认为1.0）
    edge_color	
            边的颜色（默认为黑色）
    style	
            边的样式（默认为实线，可选： solid、dashed、dotted、dashdot）
    with_labels	
            节点是否带标签（默认为True）
    font_size	
            节点标签字体大小（默认为12）
    font_color	
            节点标签字体颜色（默认为黑色）

'''
