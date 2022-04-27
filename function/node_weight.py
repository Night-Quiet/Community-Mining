from .my_function import *


def node_weight(file_name_key):
    # 不想总是改两个变量，改变filenameKey确定数据集
    # 可选择数据集名：Karate_club  Elegans_metabolic  Facebook  ErdosNet  Deezer  Amazon  Pokec
    # 数据集按节点数从小到大列出
    describe = file_name_key
    str_location_comm = "./save/connect/" + describe + "/" + describe + "_nodeConnect.csv"
    str_location_node = "./save/connect/" + describe + "/" + describe + "_node.csv"
    connect_result = read_csv(str_location_comm)
    cut_node = read_csv(str_location_node)

    cut_node_weight = dict()
    for node in cut_node:
        for comm in connect_result:
            if comm.count(node[0]):
                cut_node_weight.setdefault(node[0], 1)
                cut_node_weight[node[0]] *= len(comm)

    cut_node_weight_sort = list(cut_node_weight.items())
    cut_node_weight_sort.sort(key=lambda x: x[1], reverse=True)

    save_file_name = r"./save/result/" + describe + "/node_weight.csv"
    print_csv(save_file_name, cut_node_weight_sort)
