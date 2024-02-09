from LBCube import LBCube_n_1, LBCube_n_k
import random
import networkx as nx

def alg1(E_partition, B, F):
    # Partitioning F by dimension yields F_i
    F_partition = []
    for i in range(len(E_partition)):
        edge_i_graph = nx.Graph()
        edge_i_graph.add_edges_from(E_partition[i])
        F_i = []
        for ff in F:
            if edge_i_graph.has_edge(ff[0], ff[1]):
                F_i.append(ff)
        F_partition.append(F_i)

    # sort |F_i|
    e = []
    for i in range(len(F_partition)):
        e.append(len(F_partition[i]))
    sorted(e)

    i = 0
    while B[i] < (n - 1) * (n ** i) and i < k+1:
        i += 1
    f = i  # the delimiters of $\mathcal{B}_{k+1}$

    if f <= k:
        lambda_value = (k + 1 - f) * (n - 1) * (n ** f)
    else:
        return False


    if len(F) != lambda_value:
        return False
    else:
        # Lines 9--12
        for i in range(k+1):
            if e[i] > B[i]:
                return False
            if i < f and e[i] != 0:
                return False
            if i >= f and e[i] != (n-1) * (n ** f):
                return False
        S = []  # Line 13
        for i in range(k+1):
            if len(F_partition[i]) == (n - 1) * (n ** f):
                S.append(i)

        # Check whether one end of each remaining faulty edge in F has the same characters of length |S| with u_star (or v_star)
        e_star = random.sample(F, 1)[0]
        u_star = e_star[0]
        v_star = e_star[1]
        F.remove(e_star)
        num_1 = 1
        num_2 = 1
        for fault in F:  # Lines 16--20
            u = fault[0]
            v = fault[1]
            f_S_1 = 0
            f_S_2 = 0
            for i in S:
                if u[k-i] == u_star[k-i] or v[k-i] == u_star[k-i]:
                    f_S_1 += 1
                if f_S_1 == len(S):
                    num_1 += 1
                if u[k-i] == v_star[k-i] or v[k-i] == v_star[k-i]:
                    f_S_2 += 1
                if f_S_1 == len(S):
                    num_2 += 1

        # Line 21
        if lambda_value == num_1 or lambda_value == num_2:
            return True
        else:
            return False



if __name__ == '__main__':
    n = 4
    k = 1
    B = [0, 12]  # the restriction sequence \mathcal{B}_m and m = k+1
    f_num = 6  # the number of faulty edges
    if k == 1:
        edges = LBCube_n_1(n).edges
    else:
        edges = LBCube_n_k(n, k).edges

    # F = random.sample(list(LBC.edges), f_num)
    # print(F)
    # F = [('13', '03'), ('11', '13'), ('23', '13'), ('13', '10'), ('13', '12'), ('33', '13')]
    # F = [('13', '03'), ('03', '00'), ('33', '03'), ('23', '03'), ('03', '01'), ('01', '00'), ('23', '13')]
    F = [('22', '32'), ('00', '20'), ('23', '13'), ('23', '33'), ('03', '23'), ('20', '10'), ('12', '22'), ('21', '11'), ('20', '30'), ('02', '22'), ('01', '21'), ('21', '31')]

    if alg1(edges, B, F):
        print("F is a minimum C-restrict-cut")
    else:
        print("F is not a minimum C-restrict-cut")
