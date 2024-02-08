import random
from LBCube import LBCube_n_1, LBCube_n_k
import numpy as np
import networkx as nx
from multiprocessing import Pool
import xlwt
import time

def simulate_link(n, k, f):  # BC_{n,k} and f: the delimiter of $\mathcal{B}_m$
    if k == 1:
        edges = LBCube_n_1(n).edges
        edge_set = []
        K = []
        for i in range(k+1):
            K.append(i)
        K_f = random.sample(K, k+1-f)  # Randomly select edges of dimension k+1-f are restricted
        for i in K_f:
            edge_set.extend(edges[i])
    else:
        edges = LBCube_n_k(n, k).edges
        edge_set = []
        K = []
        for i in range(k + 1):
            K.append(i)
        K_f = random.sample(K, k + 1 - f)
        for i in K_f:
            edge_set.extend(edges[i])

    LBCube = nx.Graph()
    for i in range(len(edges)):
        LBCube.add_edges_from(edges[i])

    # Randomly select faulty edges and determine whether BC is connected or not
    FF = []
    while nx.is_connected(LBCube):
        F = random.sample(edge_set, 1)
        for link in F:
            FF.append(link)
            edge_set.remove(link)
        LBCube.remove_edges_from(F)

    return len(FF)


def test_core(n, k, f, testnum):
    Sum = []
    for i in range(testnum):
        num_f = simulate_link(n, k, f)
        Sum.append(num_f)

    return Sum

# multi-processes
def pool_core(n, k, f, testnum, processes_num):
    ptestNum = int(testnum / processes_num)
    pool = Pool(processes=processes_num)
    ress = []
    for i in range(processes_num):
        res = pool.apply_async(test_core, (n, k, f, ptestNum))
        ress.append(res)
    pool.close()
    pool.join()
    Sum = []
    for res in ress:
        x = res.get()
        for x1 in x:
            Sum.append(x1)

    tx = np.array(Sum)
    mean_f = np.mean(tx)
    median_f = np.median(tx)
    max_f = int(np.max(tx))
    counts = np.bincount(tx)
    mode_f = np.argmax(counts)

    # record data
    s1 = "bcube({0},{1},{2})_link.xls".format(n, k, f)
    bcube = xlwt.Workbook(encoding='utf-8')
    sheet1 = bcube.add_sheet('bcube', cell_overwrite_ok=True)

    sheet1.write(0, 0, 'mean')
    sheet1.write(0, 1, 'median')
    sheet1.write(0, 2, 'mode')
    sheet1.write(0, 3, 'max')

    sheet1.write(1, 0, mean_f)
    sheet1.write(1, 1, median_f)
    sheet1.write(1, 2, float(mode_f))
    sheet1.write(1, 3, float(max_f))

    j = 3
    for i in range(len(Sum)):
        sheet1.write(j, 0, i)
        sheet1.write(j, 1, Sum[i])
        j = j + 1

    bcube.save(s1)



if __name__ == '__main__':
    n = 6
    k = 2
    f = 1  # delimiters of $\mathcal{B}_m$
    testnum = 100  # The number of experiments

    time_star = time.time()
    pool_core(n, k, f, testnum, 10) # 10: the number of processes
    time_end = time.time()

    print(time_end - time_star)



