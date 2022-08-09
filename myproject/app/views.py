from django.shortcuts import render
from Code.GetData import GetData, GetID
from Code.Load import loadnode, loadedge
from Code.BuildG import buildG, buildWG
from Code.Search import search, search_works, search_relations, search_asks, search_recommendations
from Code.DrawG import draw

from Code.Search import search_contain
from Code.Search import search_works
from Code.Search import search_relations
from Code.Search import search_asks
from Code.Search import search_recommendations
from Code.Search import search_detail

'''
    author	:	纪惠婷
    ID	    :	202021012061
    endtime	:	2022/6/22
'''


# 主页
def home(request):
    """
        return	:	返回主页
    """

    flag = 0
    str = "以下是本网站的功能\n"
    str1 = "电影查询：输入某个演员、导演。能查询其参与作品、导演作品\n"
    str2 = "查询关系：输入2个顶点，能查询其关系\n"
    str3 = "智能问答：能根据您的问题进行智能回答\n"
    str4 = "电影推荐：根据一部电影，推荐同类的10部电影\n"
    if request.method == "POST":
        return search_contain(request, request.POST.get('search_contain'))
    return render(request, 'all.html', locals())


# 输入某个演员、导演。能查询其参与作品、导演作品
def search_movie(request):
    """
        param   :   search_contain 人名
        function:   search_works函数
        return  :   actors, directs 出演作品和导演作品

        add     :   在网页中的top
        return	:	BOX3_1.html
    """
    actor_works, direct_works = [], []
    search_movie_question = 0
    is_contain = 0
    if request.method == "POST":
        if 'go' in request.POST:
            return search_contain(request, request.POST.get('search_contain'))
        search_movie_question = 1
        contain = request.POST.get('search_contain')
        # --------------------------------------------
        actors, directs = search_works(contain)
        # --------------------------------------------
        actor_works, direct_works = [], []
        for i in range(len(actors)):
            actor_works.append([actors[i], 80 + 20 * i])
        for i in range(len(directs)):
            direct_works.append([directs[i], 80 + 20 * i])
        if actor_works == []:
            actor_works = [["无", 80]]
        if direct_works == []:
            direct_works = [["无", 80]]
    return render(request, 'BOX3_1.html', locals())


# 查询关系
def search_relation(request):
    """
        param   :   input1,input2  两个人名
        function:   search_relations
        return  :   path 两个人之间的联系

        add     :   在网页中的left
        return	:	BOX3_2.html
    """
    is_contain = 0
    if request.method == "POST":
        if 'go' in request.POST:
            return search_contain(request, request.POST.get('search_contain'))
        input1 = request.POST['input1']
        input2 = request.POST['input2']
        # --------------------------------------------
        path = search_relations(input1, input2)
        # --------------------------------------------
        if path == []:
            is_contain = 1
            return render(request, 'BOX3_2.html', locals())
        road = []
        x, y = GetData()
        name_id, id_name = GetID(y)
        del path[0]
        length = (1980 - (150 + (80 + 150) * len(path))) / 2
        print("length = ", length)
        length_input1 = length

        for pa in path:
            road.append([pa[1], id_name[pa[0]], length + 150])
            length += 230
        is_contain = 2
        print(road)
    return render(request, 'BOX3_2.html', locals())


# 智能问答
def search_ask(request):
    """
        param   :   input,ask1,ask2  Input类型的ask1的ask2有哪些
        function:   search_asks
        return  :   ans 只能回答的答案

        add     :   在网页中的top
                    is_contain:
                                0 —— 没有问题
                                1 —— 问题没填
                                2 —— 问题没答案
                                3 —— 有答案
        return	:	BOX3_3.html
    """
    is_contain = 0
    if request.method == "POST":
        if 'go' in request.POST:
            return search_contain(request, request.POST.get('search_contain'))
        else:
            if 'input1' not in request.POST or 'ask1' not in request.POST or 'ask2' not in request.POST:
                is_contain = 1
            else:
                is_contain = 2
                input1 = request.POST['input1']
                ask1 = request.POST['ask1']
                ask2 = request.POST['ask2']
                # --------------------------------------------
                ans = search_asks(ask1, ask2, input1)
                # --------------------------------------------
                if ans == []:
                    ans = "无结果，请重新搜索"
                else:
                    is_contain = 3
                    ans2 = []
                    if isinstance(ans, list):
                        for i in ans:
                            if isinstance(i, list):
                                for j in i:
                                    ans2.append(j)
                            else:
                                ans2.append(i)
                    else:
                        ans2 = ans
                    length = []
                    l = (1980 - min(len(ans2), 7) * 220) / 2
                    for i in range(len(ans2)):
                        if i and i % 7 == 0:
                            l -= 220 * 7
                        length.append([ans2[i], l, 430 + i // 7 * 100])
                        l += 220

    return render(request, 'BOX3_3.html', locals())


# 智能推荐
def search_recommendation(request):
    """
        param   :   input 电影名字
        function:   search_recommendations
        return  :   ans 10部电影和共同联系
        return	:	返回主页

        add     :   在网页中的left
        return	:	BOX3_4.html
    """
    if request.method == "POST":
        if 'go' in request.POST:
            return search_contain(request, request.POST.get('search_contain'))
        else:
            input = request.POST['input']
            # --------------------------------------------
            ans = search_recommendations(input)
            # --------------------------------------------
            '''
                ans:
                    [ [movie,[relaiton,relaitontype,relaiton,relationtype,...]],  [movie2,……] ]
            '''
            # 防止不够10部电影
            for i in range(10 - len(ans)):
                ans.append(['无', ['无', '']])
            # 把relation和relationtype封装在一起
            for each in ans:
                reason = each[1]
                new_reason = "\n\n\n\n推荐理由：\n"
                for i in range(len(reason) // 2):
                    new_reason += " · 共同" + reason[2 * i + 1] + "："
                    new_reason += reason[2 * i]
                    new_reason += "\n"
                each[1] = new_reason
            # ans分为ans1和ans2
            ans1 = ans[:5]
            ans2 = ans[5:]
            # 加入left元素
            for i in range(len(ans1)):
                ans1[i].append(i * 350)
            for i in range(len(ans2)):
                ans2[i].append(i * 350)

            '''
                ans:
                    [ [movie, reason, lef], [……] ]
            '''
    return render(request, 'BOX3_4.html', locals())



from Code.Ordernum import NUM

def search_details(request):
    is_contain = 0
    if request.method == "POST":
        if 'go' in request.POST:
            return search_contain(request, request.POST.get('search_contain'))
        is_contain = 1
        movie = request.POST['input']
        line = search_detail(movie)
        if line == []:
            information1 = "无此电影信息，请重新查询"
            information2 = "无此电影信息，请重新查询"
            information3 = "无此电影信息，请重新查询"
            return render(request, 'BOX3_5.html', locals())
        for i in range(len(line)):
            if isinstance(line[i], list):
                element = ""
                for each in line[i]:
                    element += "                    " + each + '\n'
                line[i] = element
            else:
                line[i] =  "                    " + line[i] + '\n'
        information1 = ""
        information2 = ""
        information3 = ""
        information1 += "\n\n名称\n" + line[0]
        information1 += "\n\n上映年份\n" + line[1]
        information1 += "\n\n评分\n" + line[2]
        information1 += "\n\n评价人数\n" + line[3]
        information1 += "\n\n导演\n" + line[4]
        information1 += "\n\n编剧\n" + line[5]
        information2 += "\n\n主演\n" + line[6]
        information3 += "\n\n类型\n" + line[7]
        information3 += "\n\n国家/地区\n" + line[8]
        information3 += "\n\n语言\n" + line[9]
        information3 += "\n\n时长\n" + line[10]
    return render(request, 'BOX3_5.html', locals())
