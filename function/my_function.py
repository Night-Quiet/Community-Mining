import csv
import networkx as nx
import pickle
import platform
from collections import Counter
import json
import copy


def csv_g(file_in):
    """
    :param file_in: csv边文件
    :return: graph: 图G
    """
    """将csv边文件-->图G"""
    """
    举例(边文件为Facebook.csv, 文件位置为相对performance.py的data文件夹中):
        G = Csv_G("./data/Facebook.csv")  此时G为以Facebook.csv边文件生成的图nx.Graph()
    """
    with open(file_in, encoding='utf-8-sig') as f:
        graph = nx.Graph()
        reader = csv.reader(f)
        for header_row in reader:
            item = header_row
            graph.add_edge(item[0], item[1], weight=1.0)
    return graph


def txt_csv(txt_filename, csv_filename, txt_type=0, csv_type=0, node=0, sp=" "):
    """
    :param txt_filename: Txt文件路径
    :param csv_filename: 自定义Csv文件路径
    :param txt_type: 0: Txt为边文件，1：Txt为其他类型文件. 可不选，默认为0
    :param csv_type: 0：Csv为边文件，1：Csv为邻接表文件. 可不选，默认为0
    :param node: 0：点不转换成真实名，1：点转换成真实名
    :param sp: Txt边文件的切分方式，如:"\t", " ". 可不选，默认为" "
    :return: Csv文件
    """
    """只有前两个参数时，为txt边文件转换成csv边文件"""
    """
    举例(欲处理Facebook.txt文件, 文件位置为相对performance.py的data文件夹中):
        如果Facebook.txt为边文件，您希望储存后csv的文件也为边文件
            txt_csv("./data/Facebook.txt", "./data/Facebook_trans.csv")  data文件夹下将生成Facebook_trans.csv文件
        如果Facebook.txt为老师的那种文件，您希望储存后的csv的文件为边文件
            txt_csv("./data/Facebook.txt", "./data/Facebook_trans.csv", 1)  data文件夹下将生成Facebook_trans.csv文件
            如果想将txt换成的csv文件使用节点的真实名字而不是编号，则
                txt_csv("./data/Facebook.txt", "./data/Facebook_trans.csv", 1, 0, 1)  data文件夹下将生成Facebook_trans.csv文件
                
        如果Facebook.txt为边文件，您希望储存后csv的文件为邻接表文件
            txt_csv("./data/Facebook.txt", "./data/Facebook_trans.csv", 0, 1): data文件夹下将生成Facebook_trans.csv文件
        
    其他同理
    """
    if txt_type == 0:
        if csv_type == 0:
            """Txt边文件-->Csv边文件"""
            list_file = []
            with open(txt_filename, "r") as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    line = line.strip(" ")
                    if len(line) != 0:
                        item = line.split(sp)
                        list_file.append([item[0], item[1]])
            with open(csv_filename, 'w', newline="", encoding='utf-8-sig') as f:
                f_csv = csv.writer(f)
                f_csv.writerows(list_file)

        if csv_type == 1:
            """Txt边文件-->Csv邻接表文件"""
            dict_file = {}
            with open(txt_filename, "r") as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    line = line.strip(" ")
                    item = line.split(sp)
                    dict_file.setdefault(item[0], []).append(item[1])
                    dict_file.setdefault(item[1], []).append(item[0])
            with open(csv_filename, 'w', newline="", encoding='utf-8-sig') as f:
                f_csv = csv.writer(f)
                for key, value in dict_file.items():
                    if not isinstance(key, list):
                        f_csv.writerow([key])
                    else:
                        f_csv.writerow(key)
                    if not isinstance(value, list):
                        f_csv.writerow([value])
                    else:
                        f_csv.writerow(value)

    if txt_type == 1:
        if csv_type == 0:
            """Txt其他类型文件-->Csv边文件"""
            node_dict = {}
            edge_list = []
            with open(txt_filename, "r") as f:
                judge_node = False
                judge_edge = False
                for line in f.readlines():
                    line = line.strip('\n')
                    line = line.strip(" ")
                    line = line.strip("\'")
                    if (not judge_node and line.find("Vertices") != -1) or line.find("Arcslist") != -1:
                        judge_node = not judge_node
                        continue
                    if not judge_edge and line.find("Edgeslist") != -1:
                        judge_edge = not judge_edge
                        continue
                    if judge_node:
                        item = line.split(" ", 1)
                        node_dict[item[0].strip("\"")] = item[1].strip("\"")
                    if judge_edge:
                        item = line.split(" ")
                        if node == 0:
                            for val in item[1:]:
                                edge_list.append([item[0], val])
                        else:
                            for val in item[1:]:
                                edge_list.append([node_dict[item[0]], node_dict[val]])
            with open(csv_filename, 'w', newline="", encoding='utf-8-sig') as f:
                f_csv = csv.writer(f)
                f_csv.writerows(edge_list)

        if csv_type == 1:
            """Txt其他类型文件-->Csv邻接表文件"""
            node_dict = {}
            edge_dict = {}
            with open(txt_filename, "r") as f:
                judge_node = False
                judge_edge = False
                for line in f.readlines():
                    line = line.strip('\n')
                    line = line.strip(" ")
                    line = line.strip("\'")
                    if (not judge_node and line.find("Vertices") != -1) or line.find("Arcslist") != -1:
                        judge_node = not judge_node
                        continue
                    if not judge_edge and line.find("Edgeslist") != -1:
                        judge_edge = not judge_edge
                        continue
                    if judge_node:
                        item = line.split(" ", 1)
                        node_dict[item[0].strip("\"")] = item[1].strip("\"")
                    if judge_edge:
                        item = line.split(" ")
                        if node == 0:
                            edge_dict.setdefault(item[0], []).extend(item[1:])
                            for val in item[1:]:
                                edge_dict.setdefault(val, []).append(item[0])
                        else:
                            edge_dict.setdefault(node_dict[item[0]], []).extend([node_dict[val] for val in item[1:]])
                            for val in item[1:]:
                                edge_dict.setdefault(node_dict[val], []).append(node_dict[item[0]])

            with open(csv_filename, 'w', newline="", encoding='utf-8-sig') as f:
                f_csv = csv.writer(f)
                for key, value in edge_dict.items():
                    if not isinstance(key, list):
                        f_csv.writerow([key])
                    else:
                        f_csv.writerow(key)
                    if not isinstance(value, list):
                        f_csv.writerow([value])
                    else:
                        f_csv.writerow(value)


def csv_csv(filename, filename_use, tran=0):
    """
    :param filename: Csv文件路径
    :param filename_use: 自定义Csv文件路径
    :param tran: 0：边文件->邻接表，1：邻接表->边文件
    :return: Csv文件
    """
    """对于边文件和邻接表文件的相互转换"""
    """
    举例(欲处理Facebook.csv文件, 文件位置为相对performance.py的data文件夹中):
        如果Facebook.csv为边文件
            csv_csv("./data/Facebook.csv", "./data/Facebook_trans.csv")  data文件夹下将生成Facebook_trans.csv文件
        如果Facebook.csv为邻接表文件
            csv_csv("./data/Facebook.csv", "./data/Facebook_trans.csv", 1)  data文件夹下将生成Facebook_trans.csv文件
    """
    if tran == 0:
        """Csv边文件-->Csv邻接表文件"""
        with open(filename, encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            list_csv = {}
            # judge = True
            for header_row in reader:
                item = header_row
                list_csv.setdefault(item[0], []).append(item[1])
                list_csv.setdefault(item[1], []).append(item[0])
        with open(filename_use, 'w', newline="", encoding='utf-8-sig') as f:
            f_csv = csv.writer(f)
            for key, value in list_csv.items():
                if not isinstance(key, list):
                    f_csv.writerow([key])
                else:
                    f_csv.writerow(key)
                if not isinstance(value, list):
                    f_csv.writerow([value])
                else:
                    f_csv.writerow(value)

    if tran == 1:
        list_data = []
        with open(filename, encoding='utf-8-sig') as f:
            f_csv = csv.reader(f)
            numJudge = 0
            keyJudge = 0
            for row in f_csv:
                if numJudge % 2 == 0:
                    keyJudge = row[0]
                else:
                    for x in row:
                        if x != "":
                            if [keyJudge, x] not in list_data and [x, keyJudge] not in list_data:
                                list_data.append([keyJudge, x])
                numJudge += 1
        with open(filename_use, 'w', newline="", encoding='utf-8-sig') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(list_data)


def read_csv(filename, csv_type=0):
    """
    :param filename: Csv文件路径
    :param csv_type: 0：划分结果文件，1：边文件，2：邻接表文件. 默认为0
    :return: 字典dict(): 邻接表
    """
    """划分结果文件，读成划分结果列表[[第一个划分], [第二个划分], [第三个划分]]"""
    """邻接表文件或边文件，读取成邻接表dict()"""
    """
    举例(欲读取文件为Facebook.csv文件, 文件位置为相对performance.py的data文件夹中):
        如果Facebook.csv为划分结果文件
            list_read = read_csv("./data/Facebook.csv")  list_read形态为[[node1, node2], [node3, node4], [node5]]
        如果Facebook.csv为边文件
            dict_read = read_csv("./data/Facebook.csv", 1)  dict_read形态为{"node1":["node2","node3"]}
        如果Facebook.csv为邻接表文件
            dict_read = read_csv("./data/Facebook.csv", 2)  dict_read形态为{"node1":["node2","node3"]}
    """
    if csv_type == 0:
        list_data = []
        with open(filename, encoding='utf-8-sig') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                list_data.append([x for x in row if x != ""])
            return list_data
    if csv_type == 1:
        """Csv边文件-->字典"""
        dict_data = {}
        reader = csv.reader(filename)
        for header_row in reader:
            item = header_row
            dict_data.setdefault(item[0], []).append(item[1])
            dict_data.setdefault(item[1], []).append(item[0])
        return dict_data
    if csv_type == 2:
        """Csv邻接表文件-->字典"""
        dict_data = {}
        with open(filename, encoding='utf-8-sig') as f:
            f_csv = csv.reader(f)
            numJudge = 0
            keyJudge = 0
            for row in f_csv:
                if numJudge % 2 == 0:
                    keyJudge = row[0]
                else:
                    dict_data[keyJudge] = [x for x in row if x != ""]
                numJudge += 1
        return dict_data


def print_csv(file, data, num_judge=0):
    """
    :param file: 存储文件路径
    :param data: 存储数据
    :param num_judge: 0：存储数据类型为[["", ""], ["", ""]]，1：存储数据类型为["", "", ""]. 默认为0
    :return: csv数据文件
    """
    """结果列表写入文件csv"""
    with open(file, 'w', newline="") as f:
        f_csv = csv.writer(f)
        if num_judge == 0:
            f_csv.writerows(data)
        if num_judge == 1:
            for val in data:
                f_csv.writerow([val])


def key_value_all(dict_in):
    """
    :param dict_in: 字典数据: {key: value}
    :return: dict_out: 字典结果: {value: key}
    """
    """单纯的字典key-value互换"""
    dict_out = {}
    for key, value in dict_in.items():
        dict_out.setdefault(value, []).append(key)
    return dict_out


def value_key_all(list_in):
    """
    :param list_in: 列表数据: [[], [], []]
    :return: dict_list: 字典结果: {0:[], 1:[], 2:[]}
    """
    """给予列表数据索引"""
    group = -1
    dict_list = dict()
    for node_list in list_in:
        group += 1
        for node in node_list:
            dict_list[node] = group
    return dict_list


def dump_object(object_in, filename):
    """
    :param object_in: 图G文件
    :param filename: 自定义文件路径
    :return: graph文件
    """
    """图G变量存储成文件"""
    f = open(filename, 'wb')
    pickle.dump(object_in, f)
    f.close()


def load_object(filename):
    """
    :param filename: graph文件路径
    :return: 图G
    """
    """图G文件转换成变量"""
    f = open(filename, 'rb')
    obj = pickle.load(f, encoding='bytes')
    f.close()
    return obj


def path_sys(str_sys):
    """
    :param str_sys: 路径字符串
    :return: str_sys: 因系统更改的路径字符串
    """
    """对文件路径字符串进行电脑系统适配"""
    if platform.system() == "Windows":
        str_sys = str_sys.replace("\\", "\\")
    else:
        str_sys = str_sys.replace("\\", "/")
    return str_sys


def modularity(g, comm, over_set=0):
    """
    :param g: 图G
    :param comm: 社区划分结果, 应为 [[], [], []]
    :param over_set: 0：非重叠模块度计算，1：重叠模块度计算
    :return: result: 模块度结果
    """
    """优化并加快模块度计算"""
    if over_set == 0:
        """社区划分模块度计算"""
        m = g.number_of_edges()
        sum_add = 0
        for node_list in comm:
            e_add = 0
            a_add = 0
            for num, node_1 in enumerate(node_list):
                a_add += g.degree(node_1)
                for node_2 in node_list[num:]:
                    if g.has_edge(node_1, node_2):
                        e_add += 1
            sum_add += (e_add / m - (a_add / (2 * m)) ** 2)
        result = sum_add
        return result

    if over_set == 1:
        """重叠社区划分模块度计算"""

        def comm_weight(result_list):
            result_temp = []
            for list_temp in result_list:
                result_temp.extend(list_temp)
            return dict(Counter(result_temp))

        weight = comm_weight(comm)
        m = g.number_of_edges()
        aij = 0
        kij = 0
        for node_list in comm:
            node_len = len(node_list)
            for node_index_1 in range(node_len):
                for node_index_2 in range(node_len):
                    node_1 = node_list[node_index_1]
                    node_2 = node_list[node_index_2]
                    kij += (g.degree(node_1) * g.degree(node_2) / (2 * m)) / (weight[node_1] * weight[node_2])
                    if g.has_edge(node_1, node_2):
                        aij += 1 / (weight[node_1] * weight[node_2])
        eq = (aij - kij) / (2 * m)
        return eq


def json_read(path):
    """
    :param path: json文件地址(相对|绝对)  此处相对地址
    :return: json对应数据集(maybe list dict)  此处得到list
    """
    """将json文件读成可使用变量"""
    with open(path, 'r', encoding='utf-8') as f:
        ts = f.read()
        list_data = json.loads(ts)
        f.close()
    return list_data


def json_save(path, dict_data):
    """
    :param path: 储存地址
    :param dict_data: 储存内容
    :return: None
    """
    """将数据储存成json文件"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dict_data, f, indent=1)
        f.close()


def api_true(g, my_result, true_result, choice=0):
    """
    :param g: 图G
    :param my_result: 自身算法的社区划分结果: [[], [], []]
    :param true_result: 真实社区划分结果: [[], [], []]
    :param choice: choice: 0: 公式优化后的计算方式，1: 原版公式的计算方式. 默认为0
    :return: API聚类效果评价指标结果
    """
    """基于公式优化后，可以快速计算出社区API聚类效果指标，但保留原公式操作以防不测"""
    if choice == 0:
        def cn2(data):
            return data * (data - 1) / 2

        my_set = [set(val) for val in my_result]
        true_set = [set(val) for val in true_result]
        n = cn2(len(g.nodes()))
        nij = 0
        ni = 0
        nj = 0
        for node_list in my_set:
            for node_list_2 in true_set:
                nij += cn2(len(node_list.intersection(node_list_2)))
        for node_list in my_set:
            ni += cn2(len(node_list))
        for node_list in true_set:
            nj += cn2(len(node_list))

        api = (nij - ni * nj / n) / (0.5 * (ni + nj) - ni * nj / n)
        return api

    if choice == 1:
        def list_dict(list1):
            dict1 = dict()
            for index, list1_one in enumerate(list1):
                for list1_one_one in list1_one:
                    dict1[list1_one_one] = index
            return dict1

        nodes = list(g.nodes())
        a00 = a01 = a10 = a11 = 0
        nodes_len = len(nodes)
        my_result_dict = list_dict(my_result)
        true_result_dict = list_dict(true_result)
        for node_index in range(nodes_len):
            for node_index_2 in range(node_index, nodes_len):
                if my_result_dict[nodes[node_index]] == my_result_dict[nodes[node_index_2]]:
                    if true_result_dict[nodes[node_index]] == true_result_dict[nodes[node_index_2]]:
                        a11 += 1
                    else:
                        a01 += 1
                else:
                    if true_result_dict[nodes[node_index]] == true_result_dict[nodes[node_index_2]]:
                        a10 += 1
                    else:
                        a00 += 1
        api = (
                (a11 - ((a11 + a01) * (a11 + a10)) / (a00 + a01 + a10 + a11)) / (
                    ((a11 + a01) + (a11 + a10)) / 2 - ((a11 + a01) * (a11 + a10)) / (a00 + a01 + a10 + a11)))
        return api


def perform(g, my_result, choice=0):
    """
    :param g: 图G
    :param my_result: 社区划分结果: [[], [], []]
    :param choice: 0: 优化到极致的代码，1: 原版公式的计算方式，2: 公式优化后的计算方式。 默认为0
    :return: 社区性能指标结果
    """
    """基于公式优化后，可以快速计算出社区性能指标，但保留原公式操作以防不测"""
    g_comm = dict()
    count = 0
    my_result_copy = copy.deepcopy(my_result)
    for comm in my_result_copy:
        for node in comm:
            g_comm[node] = count
        count += 1
    node_list = list(g.nodes())
    per = 0

    if choice == 0:
        for comm in my_result_copy:
            len_comm = len(comm)
            if len_comm < 2:
                continue
            else:
                node_all = set()
                for node in comm[::-1][1:]:
                    node_nei = set(list(g.neighbors(node)))
                    node_one = comm.pop()
                    node_all.add(node_one)
                    per += len(node_all) - len(node_all.intersection(node_nei))
        for node_1, node_2 in g.edges():
            if g_comm[node_1] != g_comm[node_2]:
                per += 1
        per = 1 - 2 * per / (len(node_list) * (len(node_list) - 1))

    if choice == 1:
        for node_index_1 in range(len(node_list)):
            for node_index_2 in range(node_index_1, len(node_list)):
                node_1 = node_list[node_index_1]
                node_2 = node_list[node_index_2]

                judge1 = g.has_edge(node_1, node_2)

                judge2 = g_comm[node_1] == g_comm[node_2]

                if judge1 and judge2:
                    per += 1
                elif (not judge1) and (not judge2):
                    per += 1

        per = 2 * per / (len(node_list) * (len(node_list) - 1))

    if choice == 2:
        for comm in my_result_copy:
            len_comm = len(comm)
            if len_comm < 2:
                continue
            else:
                for node_index_1 in range(len_comm):
                    for node_index_2 in range(node_index_1 + 1, len_comm):
                        node_1 = comm[node_index_1]
                        node_2 = comm[node_index_2]
                        if not g.has_edge(node_1, node_2):
                            per += 1
        for node_1, node_2 in g.edges():
            if g_comm[node_1] != g_comm[node_2]:
                per += 1
        per = 1 - 2 * per / (len(node_list) * (len(node_list) - 1))

    return per


def print_per(g, result, describe):
    """
    :param g: 图G
    :param result: 社区划分结果: [[], [], []]
    :param describe: 必要的描述. 可为空
    :return: 社区划分的各种指标打印
    """
    print(describe + "-----------------------------------------------")
    # print("模块性: " + str(qua.modularity(g, result)))
    print("性能: " + str(perform(g, result)))
    # print("覆盖率: " + str(qua.coverage(g, result)))
