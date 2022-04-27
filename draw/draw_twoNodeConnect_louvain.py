import math

from function.my_function import *
import community as community_louvain
import copy
import networkx as nx
from networkx.algorithms.community import asyn_lpa_communities as LPA
import os
from collections import defaultdict

"""
画图代码没注释，实在抱歉，有需要补
"""


# 可选择数据集名：Karate_club  Elegans_metabolic  Facebook  ErdosNet  Deezer  Amazon  Pokec
# 数据集按节点数从小到大排序
file_name_key = "Karate_club"
file_name = "./data/" + file_name_key + ".csv"
G = csv_g(file_name)
dump_object(G, "./file/all.graph")
# 原始的社区结构g
g = load_object('./file/all.graph')
# 聚点社区结构g_gather
file_name_gather = "./save_new/" + file_name_key + "/gNew.graph"
g_gather = load_object(file_name_gather)

file_node_weight = "./save_new/" + file_name_key + "/node_weight.csv"
file_lv_gather = "./save_new/" + file_name_key + "/lv_gather.csv"
file_node = "./save_new/" + file_name_key + "/node.csv"
file_endResult = "./save_new/" + file_name_key + "/endResult.csv"
file_nodeComm = "./save_new/" + file_name_key + "/nodeComm.json"
file_commNode = "./save_new/" + file_name_key + "/commNode.json"
file_bigOneLen = "./save_new/" + file_name_key + "/bigOne.csv"
file_gatherComm = "./save_new/" + file_name_key + "/gather_comm.json"
file_connect = "./save_new/" + file_name_key + "/connect.csv"

node_weight = read_csv(file_node_weight)
lv_gather = read_csv(file_lv_gather)
node = read_csv(file_node)
endResult = read_csv(file_endResult)
nodeComm = json_read(file_nodeComm)
commNode = json_read(file_commNode)
bigOne = read_csv(file_bigOneLen)
bigOneLen = len(bigOne)
gatherComm = json_read(file_gatherComm)
connect = read_csv(file_connect)


# 通过更改set_choice，选择制作哪张图的gexf文件，制作好后，在Gephi按照group进行节点颜色渲染，按照size进行节点大小渲染
set_choice = 6

# 第一个图---对应 制图文件夹1号图
if set_choice == 1:
    g_new = nx.Graph()
    cutNode_collect = dict()
    count = 0
    commNode_change = dict()
    node_collect = list()
    for gatherNode, cutNode_weight in commNode.items():
        count += 1
        if count > bigOneLen:
            commNode_change[gatherNode] = cutNode_weight
        else:
            for cutNode, weight in cutNode_weight.items():
                cutNode_collect.setdefault(cutNode, 0)
                cutNode_collect[cutNode] += weight
    commNode_change["C0'"] = cutNode_collect

    for gatherNode, cutNode_weight in commNode_change.items():
        for cutNode, weight in cutNode_weight.items():
            g_new.add_edge(gatherNode, cutNode, weight=weight)
        node_collect.append(gatherNode)

    node_attributes = defaultdict(dict)
    for nodeNum, node_one in enumerate(node_collect):
        node_attributes[node_one]["group"] = nodeNum
        node_attributes[node_one]["size"] = 10
    for node_one in node:
        node_attributes[node_one[0]]["group"] = -1
        node_attributes[node_one[0]]["size"] = 5
    nx.set_node_attributes(g_new, node_attributes)
    nx.write_gexf(g_new, "../save/gexf/game1.gexf")

# 第二个图---对应 制图文件夹2号图
if set_choice == 2:
    g_new = nx.Graph()
    cutNode_collect = dict()
    count = 0
    commNode_change = dict()
    node_collect = list()
    node_attributes = defaultdict(dict)
    for gatherNode, cutNode_weight in commNode.items():
        count += 1
        if count > bigOneLen:
            commNode_change[gatherNode] = cutNode_weight
        else:
            for cutNode, weight in cutNode_weight.items():
                cutNode_collect.setdefault(cutNode, 0)
                cutNode_collect[cutNode] += weight
    commNode_change["C0'"] = cutNode_collect
    for gatherNode, cutNode_weight in commNode_change.items():
        for cutNode, weight in cutNode_weight.items():
            g_new.add_edge(gatherNode, cutNode, weight=weight)
        node_collect.append(gatherNode)

    node_collect_1 = list()
    for num in range(bigOneLen):
        node_collect_1.append("C"+str(num))
    g_new_1 = nx.Graph(g_gather.subgraph(node_collect_1))
    nodeNum = 0
    for node_one in node_collect_1:
        node_attributes[node_one]["group"] = nodeNum
        node_attributes[node_one]["size"] = 10
        nodeNum += 1

    for node_one in node_collect:
        node_attributes[node_one]["group"] = nodeNum
        node_attributes[node_one]["size"] = 10
        nodeNum += 1
    for node_one in node:
        node_attributes[node_one[0]]["group"] = nodeNum
        node_attributes[node_one[0]]["size"] = 5

    g_new = nx.union(g_new, g_new_1)
    nx.set_node_attributes(g_new, node_attributes)
    nx.write_gexf(g_new, "../save/gexf/game2.gexf")

# 第三个图---对应 制图文件夹3号图
if set_choice == 3:
    g_new = nx.Graph(g_gather)
    node_attributes = defaultdict(dict)
    for nodeNum, node_one in enumerate(g_new.nodes()):
        node_attributes[node_one]["group"] = nodeNum
        node_attributes[node_one]["size"] = 10
    nx.set_node_attributes(g_new, node_attributes)
    nx.write_gexf(g_new, "../save/gexf/game3.gexf")

# 第四个图---对应 制图文件夹4号图
if set_choice == 4:
    g_new = nx.Graph(g_gather)
    comm_divide = list()
    for gather, comm in gatherComm.items():
        comm_divide_temp = [gather]
        g_new_temp = nx.Graph(g.subgraph(comm))
        for cutNode in node:
            if g_new_temp.has_node(cutNode[0]):
                nei = list(g_new_temp.neighbors(cutNode[0]))
                for node_nei in nei:
                    g_new_temp.add_edge(gather+"-"+cutNode[0], node_nei)
                g_new_temp.remove_node(cutNode[0])
        comm_divide_temp.extend(g_new_temp.nodes)
        g_new = nx.union(g_new, g_new_temp)
        comm_divide.append(comm_divide_temp)
    node_attributes = defaultdict(dict)
    print(comm_divide)
    for nodeNum, comm in enumerate(comm_divide):
        for node_one in comm:
            node_attributes[node_one]["group"] = nodeNum
            node_attributes[node_one]["size"] = 10
    nx.set_node_attributes(g_new, node_attributes)
    nx.write_gexf(g_new, "../save/gexf/game4.gexf")

# 第五个图---对应 例子文件夹原版图1
if set_choice == 5:
    node_attributes = defaultdict(dict)
    commNum = 0
    for comm in bigOne:
        for node_one in comm:
            node_attributes[node_one]["group"] = commNum
            node_attributes[node_one]["size"] = 5
        commNum += 1
    for comm in connect[1:]:
        for node_one in comm:
            node_attributes[node_one]["group"] = commNum
            node_attributes[node_one]["size"] = 5
        commNum += 1
    for node_one in node:
        node_attributes[node_one[0]]["group"] = -1
        node_attributes[node_one[0]]["size"] = 10
    nx.set_node_attributes(g, node_attributes)
    nx.write_gexf(g, "../save/gexf/game5.gexf")

# 第六个图---对应 例子文件夹---原版图6
if set_choice == 6:
    node_commNum = dict()
    commNum_neighbor = dict()
    commNum = -1
    for comm in endResult:
        commNum += 1
        for node in comm:
            node_commNum.setdefault(node, []).append(commNum)  # node_commNum: {节点: 社区号}
            commNum_neighbor.setdefault(commNum, []).extend(g.neighbors(node))  # 邻居收集

    commNum_neighborCount = {commNum: dict(Counter(neighbor)) for commNum, neighbor in commNum_neighbor.items()}  # 邻居统计
    commNum_neighborCount_copy = copy.deepcopy(commNum_neighborCount)

    edge_add = []
    commNum_neighborCount_comm = dict()
    node_comm = {}  # {聚点: 原点集}
    for commNum, comm in enumerate(endResult):
        node_center = 0
        for node in comm:
            node_center += commNum_neighborCount_copy[commNum][node]  # 聚点自环边的权重统计
            del commNum_neighborCount_copy[commNum][node]  # 点删除，为后面聚点-聚点边做准备
            node_comm.setdefault("C" + str(commNum), []).append(node)  # 聚点对应原点集，方便以后还原
        edge_add.append(("C" + str(commNum), "C" + str(commNum), node_center / 2))
        commNum_neighborCount_comm[commNum] = dict()

    for commNum, neighborCount in commNum_neighborCount_copy.items():
        for node, weight in neighborCount.items():
            node_commNum_temp = node_commNum[node][0]
            commNum_neighborCount_comm[commNum].setdefault(node_commNum_temp, 0)
            commNum_neighborCount_comm[commNum][node_commNum_temp] += weight  # 聚点-聚点权重统计
    # 聚点-聚点权重边：相互为边，weight会加2次，但是在最后进入重建g_new时，(C0, C1)和(C1，C0)的权重不会重复添加，所以weight不需要/2
    for commNum, neighborCount in commNum_neighborCount_comm.items():
        for commNum_1, weight in neighborCount.items():
            edge_add.append(("C" + str(commNum), "C" + str(commNum_1), weight))

    g_new = nx.Graph()
    g_new.add_weighted_edges_from(edge_add)

    node_attributes = defaultdict(dict)
    for commNum, node_one in enumerate(g_new.nodes):
        node_attributes[node_one]["group"] = commNum
        node_attributes[node_one]["size"] = 10

    nx.set_node_attributes(g_new, node_attributes)
    nx.write_gexf(g_new, "../save/gexf/game6.gexf")

# 其他图，皆为利用前面的制图，在Gephi进行简单修改得到，以及visio修改得到
