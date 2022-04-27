import time
from function.my_function import *
import networkx as nx
import collections
import community as community_louvain
import copy
from collections import defaultdict


file_name = r"../data/thesis_data/Facebook_4039.csv"
G = csv_g(file_name)
dump_object(G, "../save/graph/use.graph")
g = load_object("../save/graph/use.graph")

G = nx.Graph()
G.add_node("Enter")

nodeConnect_Three_read = read_csv("../save/connect/Facebook/Facebook_edgeConnect_three.csv")          # 社区
nodeConnect_Three_read = sorted(nodeConnect_Three_read, key=lambda x: len(x), reverse=True)  # 社区 按大小排序
limit = 5                                                                                    # 社区大小大于limit才进行聚点
node_commNum = dict()
commNum_neighbor = dict()

for commNum, comm in enumerate(nodeConnect_Three_read):
    for node in comm:
        node_commNum[node] = commNum                                                         # node_commNum: {节点: 社区标签}
        commNum_neighbor.setdefault(commNum, []).extend(g.neighbors(node))                   # 邻居收集
commNum_neighborCount = {commNum: dict(Counter(neighbor)) for commNum, neighbor in commNum_neighbor.items()}  # 邻居统计

# 聚点自环权重统计
edge_add = []
commNum_neighborCount_comm = dict()
commNum_limit = 0
node_comm = {}                                                                               # {聚点: 原点集}
for commNum, comm in enumerate(nodeConnect_Three_read):
    node_center = 0
    if len(comm) > limit:                                                                    # 限制>limit才进行聚点
        for node in comm:
            node_center += commNum_neighborCount[commNum][node]                              # 聚点自环边的权重统计
            del commNum_neighborCount[commNum][node]                                         # 点删除，为后面聚点-非聚点边做准备
            g.remove_node(node)                                                              # 统计完 原图g对于该点进行删除
            node_comm.setdefault("C" + str(commNum), []).append(node)                        # 聚点对应原点集，方便以后还原
        edge_add.append(("C" + str(commNum), "C" + str(commNum), node_center / 2))
        commNum_limit = commNum                                                              # 由于前面排序过，故此处为聚点交界处
        commNum_neighborCount_comm[commNum] = dict()                                         # 目的：{聚点1:{聚点2: 权重}}

# 聚点-聚点权重统计
commNum_neighborCount_copy = copy.deepcopy(commNum_neighborCount)
for commNum, neighborCount in commNum_neighborCount_copy.items():
    if commNum <= commNum_limit:                                                              # 限制在聚点交界处
        for node, weight in neighborCount.items():
            node_commNum_temp = node_commNum[node]
            if node_commNum_temp <= commNum_limit:                                            # 限制在聚点交界处
                commNum_neighborCount_comm[commNum].setdefault(node_commNum_temp, 0)
                commNum_neighborCount_comm[commNum][node_commNum_temp] += weight              # 聚点-聚点权重统计
                del commNum_neighborCount[commNum][node]                                      # 点删除，为聚点-非聚点边做准备
                
# 聚点-聚点边：相互为边，append会加2次，故weight/2
for commNum, neighborCount in commNum_neighborCount_comm.items():
    for commNum_1, weight in neighborCount.items():
        edge_add.append(("C" + str(commNum), "C" + str(commNum_1), weight / 2))
# 聚点-非聚点边：不再进行非聚点-聚点边统计，故不需要weight/2
for commNum, neighborCount in commNum_neighborCount.items():
    if commNum <= commNum_limit:                                                              # 限制在聚点交界处
        for node, weight in neighborCount.items():
            edge_add.append(("C" + str(commNum), node, weight))
           
g.add_weighted_edges_from(edge_add)                                                           # 原图加聚点相关边

group = 0
node_attributes = defaultdict(dict)
for commNum, comm in enumerate(nodeConnect_Three_read):
    group += 1
    if commNum <= commNum_limit:                                                              # 聚点交界处前对点设置组和大小
        node_attributes["C" + str(commNum)]["group"] = group
        node_attributes["C" + str(commNum)]["size"] = 10
    else:                                                                                     # 聚点交界处后对社区设置组和大小
        for node in comm:
            node_attributes[node]["group"] = group
            node_attributes[node]["size"] = 1

nx.set_node_attributes(g, node_attributes)
nx.write_gexf(g, "../save/gexf/game.gexf")


