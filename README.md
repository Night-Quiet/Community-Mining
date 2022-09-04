## 社区挖掘算法
### 具体内容参考个人论文: 复杂网络的社区挖掘.pdf
### performance.py是算法对比程序
### bipartite.py是二部图社区挖掘算法程序
## function文件夹-connect
### 里面包含了多种连通算法
### 其中有一边连通（one-edge）、二边连通（two-edge）、二点连通（two-node）、三边连通（three-edge）算法，割点割边当然也顺便获取了，对了，这几个算法速度都尽可能做到在非多线程下，尽可能最快了，百万节点数据集在cpu下都不超过10分钟，快的鸭皮。
## function文件夹-common
### 里面包含了常见的社区挖掘算法
### 其中有slpa、bigclam、k_clique（这个调包了）
