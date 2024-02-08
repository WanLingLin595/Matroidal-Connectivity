import networkx as nx
import numpy as np
from BCube import BCube_n_k
import random
import xlwt
import time
from multiprocessing import Pool
from Performance_analysis_wires import route_path, F_select_A, F_select_B

#  similar to the function "test_situation" in Performance_analysis
def test_core(n, k, B, failure_s):
    edges = BCube_n_k(n, k).wire
    servers = BCube_n_k(n, k).server

    LBC = nx.Graph()
    for i in range(len(edges)):
        LBC.add_edges_from(edges[i])

    B_len = len(B)
    K = [i for i in range(k+1)]
    B_k = random.sample(K, B_len)
    B_res = dict()
    B_num = 0
    for i in B_k:
        B_res[i] = B[B_num]
        B_num += 1


    failure_l = 6
    failure_theory = 72
    edges_copy = edges.copy()
    edges_no = edges.copy()
    F = []
    APL = []
    ABT = []
    TFR = []
    abt, apl, tfr = route_path(LBC, servers, edges)
    ABT.append(abt)
    APL.append(apl)
    TFR.append(tfr)
    while len(F) < failure_s:
        # m = k+1
        F, remove_B_k = F_select_A(F, B_k, edges_copy, edges_no, B_res, failure_l, failure_theory)
        # m < k+1:
        # F, remove_B_k = F_select_B(F, B_k, edges_copy, edges_no, B_res, failure_l, k, failure_theory)
        LBC.remove_edges_from(F)
        for i in range(len(edges)):
            edges[i] = list(set(edges[i]) - set(F))

        edges_copy = edges.copy()
        if len(B_k) > 0:
            for kk in remove_B_k:
                B_k.remove(kk)

        F = list(F)
        abt, apl, tfr = route_path(LBC, servers, edges)
        ABT.append(abt)
        APL.append(apl)
        TFR.append(tfr)

    return ABT, APL, TFR


# Simulation of 100 experiments using a multi-process approach
def pool_core(n, k, B, failure_s, processes_num):  # processes_num: the number of processes
    pool = Pool(processes=processes_num)
    pool_set = []
    for i in range(processes_num):
        pool_i = pool.apply_async(test_core, (n, k, B, failure_s))
        pool_set.append(pool_i)
    pool.close()
    pool.join()
    APL_set = []
    ABT_set = []
    TFR_set = []
    for pool_i in pool_set:
        x, y, z = pool_i.get()
        ABT_set.append(x)
        APL_set.append(y)
        TFR_set.append(z)

    # record data
    s1 = "BC({0},{1},{2})_situationA.xls".format(n, k, failure_s)
    bcube = xlwt.Workbook(encoding='utf-8')
    sheet1 = bcube.add_sheet('bcube', cell_overwrite_ok=True)
    sheet1.write(0, 0, 'F')
    sheet1.write(0, 1, 'ABT-avg')
    sheet1.write(0, 2, 'APL-avg')
    sheet1.write(0, 3, 'RFR-avg')

    # Calculation of the average of the data
    ABT_AVG = []
    APL_AVG = []
    TFR_AVG = []
    for i in range(len(ABT_set[0])):
        ABT_i = []
        APL_i = []
        TFR_i = []
        for j in range(len(ABT_set)):
            ABT_i.append(ABT_set[j][i])
            APL_i.append(APL_set[j][i])
            TFR_i.append(TFR_set[j][i])
        tx1 = np.array(ABT_i)
        tx2 = np.array(APL_i)
        tx3 = np.array(TFR_i)
        avg1 = np.average(tx1)
        avg2 = np.average(tx2)
        avg3 = np.average(tx3)
        ABT_AVG.append(avg1)
        APL_AVG.append(avg2)
        TFR_AVG.append(avg3)

    # record data
    for i in range(1, len(ABT_AVG) + 1):
        sheet1.write(i, 1, ABT_AVG[i - 1])
        sheet1.write(i, 2, APL_AVG[i - 1])
        sheet1.write(i, 3, TFR_AVG[i - 1])

    # all data
    # for i in range(len(ABT_set)):
    #     for j in range(1, len(ABT_set[i]) + 1):
    #         sheet1.write(j, i+4, ABT_set[i][j - 1])
    #         sheet1.write(j, i + 4 + len(ABT_set), APL_set[i][j - 1])
    #         sheet1.write(j, i + 4 + 2 * len(ABT_set), TFR_set[i][j - 1])

    bcube.save(s1)


if __name__ == '__main__':
    n = 6
    k = 2
    f_l = 227
    B = [0, 2, 72]

    time_start = time.time()
    pool_core(n, k, B, f_l, 100)
    time_end = time.time()
    print('BCube(6,2)-wire:', time_end - time_start)
