from function.my_function import *
import networkx as nx
import community as community_louvain
from collections import defaultdict


file_name = r"../data/thesis_data/Facebook_4039.csv"
G = csv_g(file_name)
dump_object(G, "../save/graph/use.graph")
g = load_object("../save/graph/use.graph")

nodeConnect_read = read_csv("../save/connect/Facebook/Facebook_nodeConnect.csv")           # 社区
node_read = read_csv("../save/connect/Facebook/Facebook_node.csv")
node_read = [val[0] for val in node_read]                                         # 割点
limit = 5                                                                         # 社区大小大于limit才进行聚点
nodeConnect_read = sorted(nodeConnect_read, key=lambda x: len(x), reverse=True)   # 社区 按大小排序
node_commNum = dict()
commNum_neighbor = dict()
for commNum, comm in enumerate(nodeConnect_read):
    for node in comm:
        node_commNum[node] = commNum
        if node not in node_read:                                                 # 非割点才进行邻居收集
            commNum_neighbor.setdefault(commNum, []).extend(g.neighbors(node))
commNum_neighborCount = {commNum: dict(Counter(neighbor)) for commNum, neighbor in commNum_neighbor.items()}  # 邻居统计

edge_add = []
node_comm = {}                                                                    # {聚点: 原点集}
for commNum, comm in enumerate(nodeConnect_read):
    node_center = 0                                                               # 聚点自环边的权重统计
    if len(comm) > limit:                                                         # 限制>limit才进行聚点
        for node in comm:
            if node not in node_read:
                commNum_neighborCount[commNum].setdefault(node, 0)                # 防止node的邻居全为割点，使得这里报错
                node_center += commNum_neighborCount[commNum][node]               # 聚点自环边的权重统计
                g.remove_node(node)                                               # 统计完 原图g对于该点进行删除
                node_comm.setdefault("C" + str(commNum), []).append(node)         # 聚点对应原点集，方便以后还原
            else:
                edge_add.append(("C"+str(commNum), node, commNum_neighborCount[commNum][node]))  # 割点与聚点边权重为社区与割点的邻居次数
        edge_add.append(("C"+str(commNum), "C"+str(commNum), node_center/2))      # 聚点自环边权重
g.add_weighted_edges_from(edge_add)                                               # 同一将所有新边加入原图g

# 进行louvain算法
lv_temp = community_louvain.best_partition(g)
dict_out = {}
for key, value in lv_temp.items():
    dict_out.setdefault(value, []).append(key)
lv = [list(v) for v in dict_out.values()]

node_attributes = defaultdict(dict)
group = 0
for comm in lv:                                                                 # 对louvain的结果进行设置
    group += 1
    for node in comm:
        node_attributes[node]["group"] = group                                  # 设置不同社区不同的组
        node_attributes[node]["size"] = int(g.degree(node, weight="weight"))    # 设置每个点以度权为大小

for node in node_read:
    node_attributes[node]["group"] = 0                                          # 对割点单独设置组
    node_attributes[node]["size"] = 5                                           # 对割点单独设置大小

nx.set_node_attributes(g, node_attributes)
nx.write_gexf(g, "../save/gexf/game.gexf")                                            # 作图
