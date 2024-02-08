import random
from BCube import BCube_n_k
import numpy as np
import networkx as nx
from multiprocessing import Pool
import xlwt
import time

def simulate_switch(n, k, f): # BCube(n,k) and f: the delimiter of $\mathcal{B}_m$
    switch = BCube_n_k(n, k).switch
    switch_set = []
    K = []
    for i in range(k + 1):
        K.append(i)
    K_f = random.sample(K, k + 1 - f) # Randomly select switches of dimension k+1-f are restricted
    for i in K_f:
        switch_set.extend(switch[i])

    edges = BCube_n_k(n, k).wire

    BCube_nk = nx.Graph()
    for i in range(len(edges)):
        BCube_nk.add_edges_from(edges[i])

    # Randomly select faulty switches and determine whether BCube is connected or not
    FF = []
    while nx.is_connected(BCube_nk):
        F = random.sample(switch_set, 1)
        for s in F:
            FF.append(s)
            switch_set.remove(s)
        BCube_nk.remove_nodes_from(F)

    return len(FF)

def test_core(n, k, f, testnum):
    Sum = []
    for i in range(testnum):
        num_f = simulate_switch(n, k, f)
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
    s1 = "bcube({0},{1},{2})_switch.xls".format(n, k, f)
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

    print(time_end-time_star)



