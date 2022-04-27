from function.my_function import *
from function.twoNodeConnect_louvain import twoConnect_louvain as mn
from function.connect.oneTwoThree_edge_connect import my_all_connect as tc
import networkx.algorithms.community.quality as qua
import community as community_louvain
from networkx.algorithms.community import asyn_lpa_communities as LPA
import networkx as nx


# """
# 预处理，对数据集进行转换
txt_filename = "./data/bipartite_data/disease-gene/DG-AssocMiner_miner-disease-gene.tsv"
list_file = []
with open(txt_filename, "r") as f:
    for line in f.readlines():
        line = line.strip('\n')
        line = line.strip(" ")
        if len(line) != 0:
            item = line.split("\t")
            list_file.append([item[0], item[1], item[2]])
list_file = list_file[1:]

# 二级处理，对疾病、基因进行聚类
idToName = dict()
geneToDisease = dict()
diseaseToGene = dict()
for d_id, d_name, g_id in list_file:
    idToName[d_id] = d_name
    geneToDisease.setdefault(g_id, list()).append(d_id)
    diseaseToGene.setdefault(d_id, list()).append(g_id)

json_save("./save/bipartite/geneToDisease.json", geneToDisease)
json_save("./save/bipartite/diseaseToGene.json", diseaseToGene)


# 边处理
disease = list(diseaseToGene.keys())
gene = list(geneToDisease.keys())

g = nx.Graph()
g1 = nx.Graph()
# 疾病1和疾病2 他们的关联基因集合
# 交集 -- 求交集长度
for index1 in range(len(disease)):
    for index2 in range(index1+1, len(disease)):
        d_gen1 = set(diseaseToGene[disease[index1]])
        d_gen2 = set(diseaseToGene[disease[index2]])
        gen1AndGen2 = d_gen1 & d_gen2
        if len(gen1AndGen2) >= 2:
            g.add_edge(disease[index1], disease[index2], weight=len(gen1AndGen2))

for index1 in range(len(gene)):
    for index2 in range(index1+1, len(gene)):
        g_disease1 = set(geneToDisease[gene[index1]])
        g_disease2 = set(geneToDisease[gene[index2]])
        disease1AndDisease2 = g_disease1 & g_disease2
        if len(disease1AndDisease2) >= 2:
            g1.add_edge(gene[index1], gene[index2], weight=len(disease1AndDisease2))

dump_object(g, "./save/bipartite/disease2.graph")
dump_object(g1, "./save/bipartite/gene2.graph")
# """

# """
tc(g, 1, "disease2")
tc_use = mn(g, "disease2")

tc(g1, 1, "gene2")
tc_use1 = mn(g1, "gene2")
# """

diseaseToGene = json_read("./save/bipartite/diseaseToGene.json")
geneToDisease = json_read("./save/bipartite/geneToDisease.json")


def result_change(data, trans):
    result_return = list()
    for elements in data:
        result_temp = list()
        for element in elements:
            result_temp.extend(trans[element])
        result_temp = list(set(result_temp))
        result_return.append(result_temp)

    return result_return


def per(data1, data2):
    sum_union_len = 0
    sum_len = 0
    for val in data2:
        data2_len_record = len(val)
        sum_len += data2_len_record
        max_len_union = 0
        for val1 in data1:
            union_len_temp = len(set(val) & set(val1))
            if union_len_temp > max_len_union:
                max_len_union = union_len_temp
        sum_union_len += max_len_union

    return sum_union_len / sum_len



"""
tc_d2 = read_csv("./save/result/disease2/endResult.csv")
tc_d3 = read_csv(".//save/result/disease3/endResult.csv")
tc_d4 = read_csv("./save/result/disease4/endResult.csv")

tc_g2 = read_csv("./save/result/gene2/endResult.csv")
tc_g3 = read_csv("./save/result/gene3/endResult.csv")
tc_g4 = read_csv("./save/result/gene4/endResult.csv")

g2 = load_object("./save/bipartite/disease2.graph")
g3 = load_object("./save/bipartite/disease3.graph")
g4 = load_object("./save/bipartite/disease4.graph")

lv_temp = community_louvain.best_partition(g2)
dict_out = {}
for key, value in lv_temp.items():
    dict_out.setdefault(value, []).append(key)
lv_d2 = [list(v) for v in dict_out.values()]
print_csv("./temp/lv_d2.csv", lv_d2)

lv_temp = community_louvain.best_partition(g3)
dict_out = {}
for key, value in lv_temp.items():
    dict_out.setdefault(value, []).append(key)
lv_d3 = [list(v) for v in dict_out.values()]
print_csv("./temp/lv_d3.csv", lv_d3)

lv_temp = community_louvain.best_partition(g4)
dict_out = {}
for key, value in lv_temp.items():
    dict_out.setdefault(value, []).append(key)
lv_d4 = [list(v) for v in dict_out.values()]
print_csv("./temp/lv_d4.csv", lv_d4)

lpa_temp = LPA(g2)
lpa_d2 = [list(val) for val in lpa_temp]
print_csv("./temp/lpa_d2.csv", lpa_d2)

lpa_temp = LPA(g3)
lpa_d3 = [list(val) for val in lpa_temp]
print_csv("./temp/lpa_d3.csv", lpa_d3)

lpa_temp = LPA(g4)
lpa_d4 = [list(val) for val in lpa_temp]
print_csv("./temp/lpa_d4.csv", lpa_d4)

tc_result2 = result_change(tc_d2, diseaseToGene)
tc_result3 = result_change(tc_d3, diseaseToGene)
tc_result4 = result_change(tc_d4, diseaseToGene)

lv_result2 = result_change(lv_d2, diseaseToGene)
lv_result3 = result_change(lv_d3, diseaseToGene)
lv_result4 = result_change(lv_d4, diseaseToGene)

lpa_result2 = result_change(lpa_d2, diseaseToGene)
lpa_result3 = result_change(lpa_d3, diseaseToGene)
lpa_result4 = result_change(lpa_d4, diseaseToGene)

print(per(tc_result2, tc_result3))
print(per(tc_result3, tc_result4))

print(per(lv_result2, lv_result3))
print(per(lv_result3, lv_result4))

print(per(lpa_result2, lpa_result3))
print(per(lpa_result3, lpa_result4))

"""








