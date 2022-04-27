import networkx as nx
from function.my_function import *

# """
txt_filename = "./data/bipartite_data/unicodelang/out.unicodelang"
list_file = []
with open(txt_filename, "r") as f:
    for line in f.readlines():
        line = line.strip('\n')
        line = line.strip(" ")
        if len(line) != 0:
            item = line.split("\t")
            list_file.append([item[0], item[1]])
list_file = list_file[1:]
print(list_file[0])


# 二级处理，对演员、电影进行聚类
actorToMovie = dict()
movieToActor = dict()
for a_id, m_id in list_file:
    actorToMovie.setdefault(a_id, list()).append(m_id)
    movieToActor.setdefault(m_id, list()).append(a_id)


json_save("./save/bipartite/countryToLanguage.json", actorToMovie)
json_save("./save/bipartite/languageToCountry.json", movieToActor)

# 边处理
actor = list(actorToMovie.keys())
movie = list(movieToActor.keys())

print(len(actor))
print(len(movie))
g = nx.Graph()
g1 = nx.Graph()

for index1 in range(len(actor)):
    for index2 in range(index1+1, len(actor)):
        d_gen1 = set(actorToMovie[actor[index1]])
        d_gen2 = set(actorToMovie[actor[index2]])
        gen1AndGen2 = d_gen1 & d_gen2
        if len(gen1AndGen2) >= 2:
            g.add_edge(actor[index1], actor[index2], weight=len(gen1AndGen2))

for index1 in range(len(movie)):
    for index2 in range(index1+1, len(movie)):
        g_disease1 = set(movieToActor[movie[index1]])
        g_disease2 = set(movieToActor[movie[index2]])
        disease1AndDisease2 = g_disease1 & g_disease2
        if len(disease1AndDisease2) >= 2:
            g1.add_edge(movie[index1], movie[index2], weight=len(disease1AndDisease2))

dump_object(g, "./save/bipartite/country2.graph")
dump_object(g1, "./save/bipartite/language2.graph")
"""

# """
g = load_object("./save/bipartite/country2.graph")
g1 = load_object("./save/bipartite/language2.graph")

print(len(g1.nodes))
print(len(g1.edges))

# tc(g, 1, "country2")
# tc_use = mn(g, "country2")
#
# tc(g1, 1, "language2")
# tc_use1 = mn(g1, "language2")
# """



