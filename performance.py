import time

# from function.one_two_threeConnect import my_all_connect as TC
import networkx.generators.community as cm
import networkx.algorithms.community.quality as qua
import matplotlib.pyplot as plt
from networkx.algorithms.community import label_propagation_communities as ISLPA
from networkx.algorithms.community import asyn_lpa_communities as LPA
from networkx.algorithms.community import girvan_newman as GN
from networkx.algorithms.community import greedy_modularity_communities as CNM
from networkx.algorithms.community import asyn_fluidc as FC
import community as community_louvain
from networkx.algorithms.community.modularity_max import _naive_greedy_modularity_communities as NCNM
from function.my_function import *
from function.common.slpa import slpa
import math
import networkx as nx
from function.twoNodeConnect_louvain import twoConnect_louvain as TC
import joblib


def main():
	
	# 做G, 理论上, 做G只需要一次, 但是为了防止操作不当, 没有将其注释
	# """
	file_name = r"./data/thesis_data/Deezer.csv"
	G = csv_g(file_name)
	dump_object(G, "./save/graph/use.graph")
	# """
	G = load_object('./save/graph/use.graph')
	print("开始了")

	"""我们的算法"""
	# """
	time_begin = time.time()
	tc = TC(G, "Deezer")
	time_end = time.time()
	time_tc = time_end-time_begin
	joblib.dump(tc, "./temp/tc.joblib")
	print("tc结束")
	# """

	"""基于模块最大化的社区划分: Clauset-Newman-Moore 贪婪模块度最大化算法"""
	# time_begin = time.time()
	# cnm = CNM(G)  # cnm = {frozenset(v) for v in cnm}  # 将list转化会frozenset
	# cnm = [list(val) for val in cnm]
	# time_end = time.time()
	# time_cnm = time_end-time_begin
	# print("cnm结束")

	"""基于模块度的社区划分: Louvian 算法"""
	time_begin = time.time()
	lv_temp = community_louvain.best_partition(G)
	dict_out = {}
	for key, value in lv_temp.items():
		dict_out.setdefault(value, []).append(key)
	lv = [list(v) for v in dict_out.values()]
	time_end = time.time()
	time_lv = time_end - time_begin
	joblib.dump(lv, "./temp/lv.joblib")
	print("lv结束")

	"""用于社区检测的异步流体社区算法: Fluid Communities算法"""
	n = len(G.nodes)
	time_begin = time.time()
	k = math.floor(pow(1.7, math.log(n)))
	fc_temp = FC(G, k)
	fc = [list(val) for val in fc_temp]
	time_end = time.time()
	time_fc = time_end - time_begin
	joblib.dump(fc, "./temp/fc.joblib")
	print("fc结束")

	"""基于标签传播的非重叠社区发现算法: Label Propagation Algorithm算法"""
	time_begin = time.time()
	lpa_temp = LPA(G)
	lpa = [list(val) for val in lpa_temp]
	time_end = time.time()
	time_lpa = time_end - time_begin
	joblib.dump(lpa, "./temp/lpa.joblib")
	print("lpa结束")

	"""基于标签传播的非重叠社区发现算法: 半同步LPA算法"""
	# time_begin = time.time()
	# islpa_temp = ISLPA(G)
	# islpa = [list(val) for val in islpa_temp]
	# time_end = time.time()
	# time_islpa = time_end - time_begin
	# print("islpa结束")

	"""基于标签传播的非重叠社区发现算法的扩展: Speaker-Listener LPA算法"""
	# time_begin = time.time()
	# slpa_temp = SLPA(G, 30, 0.33)
	# slpa = [list(v) for v in slpa_temp]
	# time_end = time.time()
	# time_slpa = time_end - time_begin
	# print("slpa结束")

	"""利用渗透法在图中寻找K族群落: K-clique算法 CPM--重叠社区, 性能计算不可用"""
	# time_begin = time.time()
	# kcc_temp = KCC(G)
	# kcc = [list(val) for val in kcc_temp]
	# time_end = time.time()
	# time_kcc = time_end - time_begin
	# print("kcc结束")

	"""基于中心性概念的计算社区功能: Girvan–Newman算法--跑半年,低于一千个节点的数据集可以尝试"""
	# time_begin = time.time()
	# gn_temp = GN(G)
	# gn = [list(val) for val in next(gn_temp)]
	# time_end = time.time()
	# time_gn = time_end - time_begin
	# print("gn结束")

	"""利用贪心模块最大化方法寻找图中的社区: 没有名字--同样跑半年,低于一千个节点的数据集可以尝试"""
	# time_begin = time.time()
	# ncnm_temp = NCNM(G)
	# ncnm = [list(val) for val in ncnm_temp]
	# time_end = time.time()
	# time_ncnm = time_end - time_begin
	# print("ncnm结束")

	"""曾经性能测试的代码太过low,跑的奇慢,所以对于大型数据集的结果,先保存,保证下次测试时,不需要再跑一次社区划分结果,属于次时代的产物"""
	# tc = joblib.load("./temp/tc.joblib")
	# lpa = joblib.load("./temp/lpa.joblib")
	# lv = joblib.load("./temp/lv.joblib")
	# fc = joblib.load("./temp/fc.joblib")

	print("---------------------------------------------------")
	"""****************耗时测试****************"""
	print("我们算法运行耗时："+str(time_tc))
	# print("CNM运行耗时："+str(time_cnm))
	print("Louvian运行耗时："+str(time_lv))
	# print("Girvan–Newman运行耗时："+str(time_gn))
	print("LPA运行耗时："+str(time_lpa))
	# print("SLPA运行耗时："+str(time_slpa))
	# print("ISLPA运行耗时："+str(time_islpa))
	print("Fluid Communities运行耗时："+str(time_fc))
	print("---------------------------------------------------")

	print("---------------------------------------------------")
	"""****************性能测试****************"""
	# print(modularity(G, tc))
	print("三边连通性能："+str(perform(G, tc)))
	# print(nx.algorithms.community.quality.coverage(G, tc))
	# print("CNM性能："+str(perform(G, cnm)))
	print("Louvian性能："+str(perform(G, lv)))
	# print("Girvan–Newman性能："+str(perform(G, gn)))
	print("LPA性能："+str(perform(G, lpa)))
	# print("SLPA性能："+str(perform(G, slpa)))
	# print("ISLPA性能："+str(perform(G, islpa)))
	print("Fluid Communities性能："+str(perform(G, fc)))
	print("---------------------------------------------------")

	print("---------------------------------------------------")
	"""****************模块度测试****************"""
	print("三边连通模块度：" + str(qua.modularity(G, tc)))
	# print("CNM模块度：" + str(qua.modularity(G, cnm)))
	print("Louvian模块度：" + str(qua.modularity(G, lv)))
	# print("Girvan–Newman模块度：" + str(qua.modularity(G, gn)))
	print("LPA模块度：" + str(qua.modularity(G, lpa)))
	# print("SLPA模块度：" + str(qua.modularity(G, slpa)))
	# print("ISLPA模块度：" + str(qua.modularity(G, islpa)))
	print("Fluid Communities模块度：" + str(qua.modularity(G, fc)))
	print("---------------------------------------------------")


if __name__ == "__main__":
	main()
