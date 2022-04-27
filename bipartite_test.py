from function.my_function import *
import networkx as nx


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

idToName = dict()
geneToDisease = dict()
diseaseToGene = dict()
for d_id, d_name, g_id in list_file:
    idToName[d_id] = d_name
    geneToDisease.setdefault(g_id, list()).append(d_id)
    diseaseToGene.setdefault(d_id, list()).append(g_id)


g = nx.Graph()
edge_weight = dict()
for d_id, g_id_all in diseaseToGene.items():
    for g_id in g_id_all:
        for d_id_other in geneToDisease[g_id]:
            if d_id != d_id_other:
                edge_weight.setdefault(d_id, dict()).setdefault(d_id_other, 0)
                edge_weight[d_id][d_id_other] += 1

for d_id, d_id_other_all in edge_weight.items():
    for d_id_other, weight in d_id_other_all.items():
        g.add_edge(d_id, d_id_other, weight=weight)

print(len(g.nodes))
print(len(g.edges))
print(len(geneToDisease.keys()))

print(diseaseToGene["C0034065"])
print(diseaseToGene["C0027540"])
print(set(diseaseToGene["C0034065"]) & set(diseaseToGene["C0027540"]))
print(g.get_edge_data("C0034065", "C0027540"))
# for value in geneToDisease.values():
#     if len(value) > 5:
#         print(value)
# print(len(geneToDisease.keys()))

# nx.write_gexf(g, "./disease.gexf")


# g1 = nx.Graph()
# edge_weight1 = dict()
# for g_id, d_id_all in geneToDisease.items():
#     for d_id in d_id_all:
#         for g_id_other in diseaseToGene[d_id]:
#             if g_id != g_id_other:
#                 edge_weight1.setdefault(g_id, dict()).setdefault(g_id_other, 0)
#                 edge_weight1[g_id][g_id_other] += 1
#
# for g_id, g_id_other_all in edge_weight1.items():
#     for g_id_other, weight in g_id_other_all.items():
#         g1.add_edge(g_id, g_id_other, weight=weight)
#
# print(len(g1.nodes))
# print(len(g1.edges))

# tc(g, 1, "disease")
# mn(g, "disease")
# tc(g1, 1, "gene")
# mn(g1, "gene")


