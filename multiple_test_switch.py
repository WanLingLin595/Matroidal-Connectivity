import networkx as nx
import numpy as np
from BCube import BCube_n_k
import random
import xlwt
import time
from multiprocessing import Pool
from Performance_analysis_switch import route_path, F_select_A, F_select_B

# Similar to the function "test_core" in Performance_analysis_switch
def test_core(n, k, B, failure_s):
    edges = BCube_n_k(n, k).wire
    servers = BCube_n_k(n, k).server
    switches = BCube_n_k(n, k).switch

    LBC = nx.Graph()
    for i in range(len(edges)):
        LBC.add_edges_from(edges[i])

    B_len = len(B)
    K = [i for i in range(k + 1)]
    B_k = random.sample(K, B_len)
    B_res = dict()
    B_num = 0
    for i in B_k:
        B_res[i] = B[B_num]
        B_num += 1

    failure_l = 1
    failure_theory = 12
    switch_copy = switches.copy()
    switch_no = switches.copy()
    F = []
    APL = []
    ABT = []
    RFR = []
    abt, apl, tfr = route_path(LBC, servers, edges)
    ABT.append(abt)
    APL.append(apl)
    RFR.append(tfr)
    while len(F) < failure_s:
        # if m = k+1
        F, remove_B_k = F_select_A(F, B_k, switch_copy, switch_no, B_res, failure_l, failure_theory)
        # if m < k+1
        # F, remove_B_k = F_select_B(F, B_k, switch_copy, switch_no, B_res, failure_l, k, failure_theory)
        LBC.remove_nodes_from(F)
        for i in range(len(switch_copy)):
            switch_copy[i] = list(set(switch_copy[i]) - set(F))

        if len(B_k) > 0:
            for kk in remove_B_k:
                B_k.remove(kk)

        F = list(F)
        abt, apl, tfr = route_path(LBC, servers, edges)
        ABT.append(abt)
        APL.append(apl)
        RFR.append(tfr)

    return ABT, APL, RFR


def pool_core(n, k, B, failure_s, processes_num):
    pool = Pool(processes=processes_num)
    pool_set = []
    for i in range(processes_num):
        pool_i = pool.apply_async(test_core, (n, k, B, failure_s))
        pool_set.append(pool_i)
    pool.close()
    pool.join()
    APL_set = []
    ABT_set = []
    RFR_set = []
    for pool_i in pool_set:
        x, y, z = pool_i.get()
        ABT_set.append(x)
        APL_set.append(y)
        RFR_set.append(z)

    # 所有数据都记录
    s1 = "BC({0},{1},{2})_situation_A_switch.xls".format(n, k, failure_s)
    bcube = xlwt.Workbook(encoding='utf-8')
    sheet1 = bcube.add_sheet('bcube', cell_overwrite_ok=True)
    sheet1.write(0, 0, 'F')
    sheet1.write(0, 1, 'ABT-avg')
    sheet1.write(0, 2, 'APL-avg')
    sheet1.write(0, 3, 'RFR-avg')

    #均值计算
    ABT_AVG = []
    APL_AVG = []
    RFR_AVG = []
    for i in range(len(ABT_set[0])):
        ABT_i = []
        APL_i = []
        RFR_i = []
        for j in range(len(ABT_set)):
            ABT_i.append(ABT_set[j][i])
            APL_i.append(APL_set[j][i])
            RFR_i.append(RFR_set[j][i])
        tx1 = np.array(ABT_i)
        tx2 = np.array(APL_i)
        tx3 = np.array(RFR_i)
        avg1 = np.average(tx1)
        avg2 = np.average(tx2)
        avg3 = np.average(tx3)
        ABT_AVG.append(avg1)
        APL_AVG.append(avg2)
        RFR_AVG.append(avg3)

    # record data
    for i in range(1, len(ABT_AVG) + 1):
        sheet1.write(i, 1, ABT_AVG[i - 1])
        sheet1.write(i, 2, APL_AVG[i - 1])
        sheet1.write(i, 3, RFR_AVG[i - 1])

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
    f_l = 38
    B = [0, 0, 12]

    time_start = time.time()
    pool_core(n, k, B, f_l, 100)
    time_end = time.time()
    print('BCube(6,2)_switch:', time_end - time_start)