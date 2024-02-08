import networkx as nx
import numpy as np
from BCube import BCube_n_k
import random
import xlwt
import time


def route_path(BC, BC_server, BC_wire):
    BC_copy = BC.copy()
    BC_servers_array = np.array(BC_server)
    BC_servers = list(BC_servers_array.flatten())
    BC_edge = []
    for i in range(len(BC_wire)):
        BC_edge.extend(BC_wire[i])

    Pathes_set = dict()  # record all paths in the all-to-all traffic pattern
    for v in BC_servers:
        Pathes_set[v] = []
        bfs_path = nx.bfs_tree(BC_copy, v)
        bfs_path.add_nodes_from(BC_servers)
        Pathes_set[v].append(bfs_path)


    # Count the number of times each wire in BCube has been passed through during transmission
    edge_set = dict()
    for e in BC_edge:
        edge_set[e] = 0
    for v in BC_servers:
        V_copy = BC_servers.copy()
        V_copy.remove(v)
        for u in V_copy:
            if nx.has_path(Pathes_set[v][0], v, u):
                route_vu = nx.shortest_path(Pathes_set[v][0], v, u)
                for i in range(len(route_vu) - 1):
                    if route_vu[i] in BC_servers:
                        ee = (route_vu[i], route_vu[i + 1])
                        edge_set[ee] += 1


    # Let the bandwidth of each wire be 1Gbps
    Final_edge_times = dict()
    for e in BC_edge:
        if edge_set[e] == 0:
            Final_edge_times[e] = 0
        else:
            Final_edge_times[e] = 1 / edge_set[e]


    # Start calculating for each route
    ABT = 0
    failure_path = 0
    free_path = 0
    sum_path_length = 0
    for v in BC_servers:
        V_copy = BC_servers.copy()
        V_copy.remove(v)
        for u in V_copy:
            if nx.has_path(Pathes_set[v][0], v, u):
                free_path += 1
                path_len = nx.shortest_path_length(Pathes_set[v][0], v, u) / 2
                sum_path_length += path_len
                route_vu = nx.shortest_path(Pathes_set[v][0], v, u)
                times_set = []
                for i in range(len(route_vu) - 1):
                    if route_vu[i] in BC_servers:
                        ee = (route_vu[i], route_vu[i + 1])
                        times_vu = Final_edge_times[ee]
                        times_set.append(times_vu)
                min_vu = min(times_set)
                ABT += min_vu
            else:
                failure_path += 1

    ABT = round(ABT, 3)
    APL = sum_path_length / free_path
    RFR = failure_path / (free_path + failure_path)

    return ABT, APL, RFR



# B: the restriction sequence, that is {b_0,b_1,\ldots, b_m}
# failure_s: upper bound on the number of faulty edges
def test_situation(n, k, B, failure_s):
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
    for i in B_k:  # Randomly select dimensions for restriction
        B_res[i] = B[B_num]
        B_num += 1

    # Choose the faulty wires
    failure_l = 50   # The number of faulty wires increasing each time
    failure_theory = 72  # \lambda: Theoretical
    edges_copy = edges.copy()
    edges_no = edges.copy()
    F = []
    APL = []
    ABT = []
    RFR = []
    abt, apl, tfr = route_path(LBC, servers, edges)
    ABT.append(abt)
    APL.append(apl)
    RFR.append(tfr)
    while len(F) < failure_s:
        # if m=k+1
        F, remove_B_k = F_select_A(F, B_k, edges_copy, edges_no, B_res, failure_l, failure_theory)  # Selection method of faulty wires
        # if m<k+1
        # F, remove_B_k = F_select_B(F, B_k, edges_copy, edges_no, B_res, failure_l, k, failure_theory)
        LBC.remove_edges_from(F)
        # Process wires and remove faulty wires from LBC
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
        RFR.append(tfr)

    # recorded data
    s1 = "BC({0},{1},{2})_situationA.xls".format(n, k, len(F))
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




def F_select_A(F, B_k, edges, edges_no, B_res, failure_num, failure_theory):
    edges_copy = edges.copy()
    F_copy = F.copy()
    choose_F = []
    # At the beginning, only select the faulty wires that meet the restriction sequence B_k
    if len(B_k) > 0:
        for i in B_k:
            choose_F.extend(edges_copy[i])
    # After exceeding the upper bound of B, it is assumed that the faulty wires are randomly distributed throughout the entire network
    else:
        for i in range(len(edges_copy)):
            choose_F.extend(edges_copy[i])

    # To evaluate the performance of theoretical values \lambda
    if (len(F) + failure_num > failure_theory) and (failure_theory - len(F) > 0):
        failure_num = failure_theory - len(F)
    if (len(F) == failure_theory) and (len(F) % failure_num != 0):
        difference_num = len(F) % failure_num
        failure_num = failure_num - difference_num

    # Randomly select faulty wires
    F_one = random.sample(choose_F, failure_num)
    F.extend(F_one)

    # Judge F to evaluate whether the upper bound of B's limit has been reached
    remove_B_k = []
    for kk in B_k:
        F_k = list(set(F) & set(edges_no[kk]))
        F = list(F)
        if len(F_k) == B_res[kk]:
            remove_B_k.append(kk)
        if len(F_k) > B_res[kk]:
            gap_F = len(F_k) - B_res[kk]
            F_new = list(set(F) - set(F_copy))
            F_inter = list(set(F_new) & set(F_k))
            gap_F_set = random.sample(F_inter, gap_F)
            choose_F = list(set(choose_F) - set(edges_no[kk]))
            if len(choose_F) != 0:
                F_two = random.sample(choose_F, gap_F)
                F = list(set(F) - set(gap_F_set))
                F.extend(F_two)

            remove_B_k.append(kk)

    return F, remove_B_k


def F_select_B(F, B_k, edges, edges_no, B_res, failure_num, k, failure_theory):
    edges_copy = edges.copy()
    F_copy = F.copy()
    choose_F = []
    if len(B_k) > 0:
        for i in B_k:
            choose_F.extend(edges_copy[i])
    if len(B_k) == 0 and len(F) < failure_theory:
        B_k_ini = B_res.keys()
        K = [i for i in range(k+1)]
        B_redu = list(set(K) - set(B_k_ini))
        for i in B_redu:
            choose_F.extend(edges_copy[i])
        if (len(F) + failure_num > failure_theory) and (failure_theory - len(F) > 0):
            failure_num = failure_theory - len(F)
    if len(B_k) == 0 and len(F) >= failure_theory:
        for i in range(len(edges_copy)):
            choose_F.extend(edges_copy[i])

    if (len(F) == failure_theory) and (len(F) % failure_num != 0):
        difference_num = len(F) % failure_num
        failure_num = failure_num - difference_num

    F_one = random.sample(choose_F, failure_num)
    F.extend(F_one)

    remove_B_k = []
    for kk in B_k:
        F_k = list(set(F) & set(edges_no[kk]))
        F = list(F)
        if len(F_k) == B_res[kk]:
            remove_B_k.append(kk)
        if len(F_k) > B_res[kk]:
            gap_F = len(F_k) - B_res[kk]
            F_new = list(set(F) - set(F_copy))
            F_inter = list(set(F_new) & set(F_k))
            gap_F_set = random.sample(F_inter, gap_F)
            choose_F = list(set(choose_F) - set(edges_no[kk]))
            if len(choose_F) != 0:
                F_two = random.sample(choose_F, gap_F)
                F = list(set(F) - set(gap_F_set))
                F.extend(F_two)

            remove_B_k.append(kk)

    return F, remove_B_k






if __name__ == '__main__':
    n = 4
    k = 2
    f_l = 60 # upper bound on the number of faulty edges
    B = [0, 0, 36, 36]
    # B = [0, 4]

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
