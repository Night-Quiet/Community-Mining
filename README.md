
# 二点连通-louvain

##### 该项目主要是实现图网络聚类/社区挖掘算法: 二点连通-louvain. 
##### 具体算法描述在个人论文中: 复杂网络的社区挖掘.pdf.

## 念想

##### 当初很有梦想, 用python对着论文完美实现了三边连通, 并将其优化到接近论文描述的时间复杂度, 希望能从连通图的角度得到一个更为优秀的图网络挖掘算法.
##### 现在只能退一步, 利用连通性, 优化louvain算法, 也算是一个退让和遗憾吧
- [三边连通论文](https://xueshu.baidu.com/usercenter/paper/show?paperid=5a791af706fa9836a86af59d6778ff2f)
## 附录

### 本项目不止存了二点连通-louvain算法, 存了很多其他社区挖掘算法的个人实现.
### 算是对于社区挖掘算法所有尝试的留存本.

##### bipartite.py: 二部图社区挖掘算法程序
##### performance.py: 算法对比程序
##### function/connect: 多种连通图算法. 包括有一边连通（one-edge）、二边连通（two-edge）、二点连通（two-node）、三边连通（three-edge），割点割边. 算法尽可能的逼近论文或相关证明的时间复杂度.
##### function/common: 常见社区挖掘算法: 包括slpa、bigclam、k_clique（这个调包了, 但是其实实现也很简单）

## 截图

![算法流程图](https://github.com/Night-Quiet/Community-Mining/blob/main/%E7%AE%97%E6%B3%95%E6%B5%81%E7%A8%8B%E5%9B%BE.jpg)

