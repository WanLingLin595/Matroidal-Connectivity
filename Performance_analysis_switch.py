import networkx as nx
import numpy as np
from BCube import BCube_n_k
import random
import xlwt
import time
from Performance_analysis_wires import route_path

# B: the restriction sequence, that is {b_0,b_1,\ldots, b_m}
# failure_s: upper bound on the number of faulty switches
def test_situation(n, k, B, failure_s):
    edges = BCube_n_k(n, k).wire
    servers = BCube_n_k(n, k).server
    switches = BCube_n_k(n, k).switch

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

    # Choose the faulty switches
    failure_l = 1   # The number of faulty switches increasing each time
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
        # Process switches and remove faulty switches from LBC
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

    # 记录
    s1 = "BC({0},{1},{2})_situation_A_switch.xls".format(n, k, len(F))
    bcube = xlwt.Workbook(encoding='utf-8')
    sheet1 = bcube.add_sheet('bcube', cell_overwrite_ok=True)
    sheet1.write(0, 0, 'F')
    sheet1.write(0, 1, 'ABT')
    sheet1.write(0, 2, 'APL')
    sheet1.write(0, 3, 'RFR')

    for i in range(1, len(ABT) + 1):
        sheet1.write(i, 1, ABT[i - 1])
        sheet1.write(i, 2, APL[i - 1])
        sheet1.write(i, 3, RFR[i - 1])

    bcube.save(s1)

# Similar to the function "F_select_A" in Performance_analysis_wires
def F_select_A(F, B_k, switches, switch_no, B_res, failure_num, failure_theory):
    switch_copy = switches.copy()
    F_copy = F.copy()
    choose_F = []
    if len(B_k) > 0:
        for i in B_k:
            choose_F.extend(switch_copy[i])
    else:
        for i in range(len(switch_copy)):
            choose_F.extend(switch_copy[i])


    if (len(F) + failure_num > failure_theory) and (failure_theory - len(F) > 0):
        failure_num = failure_theory - len(F)
    if (len(F) == failure_theory) and (len(F) % failure_num != 0):
        difference_num = len(F) % failure_num
        failure_num = failure_num - difference_num

    F_one = random.sample(choose_F, failure_num)
    F.extend(F_one)

    remove_B_k = []
    for kk in B_k:
        F_k = list(set(F) & set(switch_no[kk]))
        F = list(F)
        if len(F_k) == B_res[kk]:
            remove_B_k.append(kk)
        if len(F_k) > B_res[kk]:
            gap_F = len(F_k) - B_res[kk]
            F_new = list(set(F) - set(F_copy))
            F_inter = list(set(F_new) & set(F_k))
            gap_F_set = random.sample(F_inter, gap_F)
            choose_F = list(set(choose_F) - set(switch_no[kk]))
            if len(choose_F) != 0:
                F_two = random.sample(choose_F, gap_F)
                F = list(set(F) - set(gap_F_set))
                F.extend(F_two)

            remove_B_k.append(kk)

    return F, remove_B_k



def F_select_B(F, B_k, switches, switch_no, B_res, failure_num, k, failure_theory):
    switch_copy = switches.copy()
    F_copy = F.copy()
    choose_F = []
    if len(B_k) > 0:
        for i in B_k:
            choose_F.extend(switch_copy[i])
    if len(B_k) == 0 and len(F) < failure_theory:
        B_k_ini = B_res.keys()
        K = [i for i in range(k+1)]
        B_redu = list(set(K) - set(B_k_ini))
        for i in B_redu:
            choose_F.extend(switch_copy[i])
        if (len(F) + failure_num > failure_theory) and (failure_theory - len(F) > 0):
            failure_num = failure_theory - len(F)
    if len(B_k) == 0 and len(F) >= failure_theory:
        for i in range(len(switch_copy)):
            choose_F.extend(switch_copy[i])

    if (len(F) == failure_theory) and (len(F) % failure_num != 0):
        difference_num = len(F) % failure_num
        failure_num = failure_num - difference_num

    F_one = random.sample(choose_F, failure_num)
    F.extend(F_one)

    remove_B_k = []
    for kk in B_k:
        F_k = list(set(F) & set(switch_no[kk]))
        F = list(F)
        if len(F_k) == B_res[kk]:
            remove_B_k.append(kk)
        if len(F_k) > B_res[kk]:
            gap_F = len(F_k) - B_res[kk]
            F_new = list(set(F) - set(F_copy))
            F_inter = list(set(F_new) & set(F_k))
            gap_F_set = random.sample(F_inter, gap_F)
            choose_F = list(set(choose_F) - set(switch_no[kk]))
            if len(choose_F) != 0:
                F_two = random.sample(choose_F, gap_F)
                F = list(set(F) - set(gap_F_set))
                F.extend(F_two)

            remove_B_k.append(kk)

    return F, remove_B_k





if __name__ == '__main__':
    n = 6
    k = 2
    f_l = 38 # upper bound on the number of faulty switches
    B = [0, 0, 12]

    time_start = time.time()
    test_situation(n, k, B, f_l)
    time_end = time.time()
    print(time_end-time_start)

    # edges = BCube_n_k(n, k).wire
    # servers = BCube_n_k(n, k).server
    #
    # LBC = nx.Graph()
    # for i in range(len(edges)):
    #     LBC.add_edges_from(edges[i])
    #
    #
    # abt, apl, tfr = route_path(LBC, servers, edges)
    # print(abt, apl, tfr)
