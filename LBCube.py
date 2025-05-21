import itertools
from BCube import ten2x

class Kn():   #  complete graph K_n
    def __init__(self, n):
        self.n = n
        v = []
        for i in range(n):
            vertex = ten2x(i, n, 1)
            v.append(vertex)
        self.vertexes = v  # node set
        self.edges = self.get_edges(self.vertexes)  # edge set

    def get_edges(self, vertices): # K_n is a graph in which arbitrary two distinct nodes are adjacent
       E = []
       for i in range(len(vertices)):
           u = vertices[i]
           for j in range(i+1, len(vertices)):
               v = vertices[j]
               e = (u, v)
               E.append(e)

       return E

class LBCube_n_1(): # consists of n K_n's
    # address：v_1v_0 and v_1, v_0 \in[0,n-1]
    def __init__(self, n):
        self.n = n
        self.vertex = self.nodes(self.n)
        self.edges = self.edges_construction(n, self.vertex)

    def nodes(self, n):
        v = dict()
        for i in range(n):
            v[i] = []
            for j in range(n):
                vertex = ten2x(i, n, 1) + ten2x(j, n, 1)
                v[i].append(vertex)

        return v

    def edges_construction(self, n, vertex):
        # Construct 0-dimensional edges: E_0
        E_0 = Kn(n).edges
        E_0_copy = []
        E = []

        for i in range(n):
            for e in E_0:
                u = ten2x(i, n, 1) + e[0]
                v = ten2x(i, n, 1) + e[1]
                ee = (u, v)
                E_0_copy.append(ee)

        E.append(E_0_copy)

        # Construct 1-dimensional edges: E_1
        E_1 = []
        for i in range(len(vertex)):
            for u in vertex[i]:
                for j in range(i+1, len(vertex)):
                    for v in vertex[j]:
                        if u[1] == v[1]:
                            e = (u, v)
                            E_1.append(e)

        E.append(E_1)

        return E


class LBCube_n_k():
   # Constructed on the basis of LBCube_n_1
   # address： v_k v_k-1 \ldots v_1 v_0   v_i\in[0,n-1]

   def __init__(self, n, k):
       if k > 1:
          self.n = n
          self.k = k
          self.vertex = self.nodes(n, k)
          self.edges = self.get_edges(n, k, self.vertex)

   def nodes(self, n, k):
       BCube_n_1 = LBCube_n_1(n)
       v = BCube_n_1.vertex

       u = dict() # record all nodes
       for i in range(1, k):
           for j in range(n):
               u[j] = []
               for a in range(n):
                   for b in range((n)*(n**(i-1))):
                      vertex = ten2x(j, n, 1) + v[a][b]
                      u[j].append(vertex)
           v = u.copy()

       return u

   def get_edges(self, n, k, vertex_set):
       E = []  # record all edges
       for i in range(k):  # Consider 0--(k-1)-dimensional edges
           EE = []
           for j in range(len(vertex_set)):
               vertex_set_copy = vertex_set[j].copy()
               while len(vertex_set_copy) > 0:
                   u_set = []
                   for add in range(n):
                       ver = vertex_set_copy[0][0:k-i] + str(add) + vertex_set_copy[0][k-i+1:]
                       u_set.append(ver)
                   for uu in u_set:
                       vertex_set_copy.remove(uu)
                   u_edge = itertools.combinations(u_set, 2)
                   for edges in u_edge:
                       EE.append(edges)
           E.append(EE)

       vertex_set_all = []
       for i in range(len(vertex_set)):
           vertex_set_all.extend(vertex_set[i])

       # Consider k-dimensional edges
       EE = []
       while len(vertex_set_all) > 0:
           u_set = []
           for add in range(n):
               ver = str(add) + vertex_set_all[0][1:]
               u_set.append(ver)
           for uu in u_set:
               vertex_set_all.remove(uu)
           u_edge = itertools.combinations(u_set, 2)
           for edges in u_edge:
               EE.append(edges)

       E.append(EE)

       return E


class LBCube_switch():
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.switch = self.switches(n, k)

    def switches(self, n, k):
        adss = []
        if k == 1:
            adss = []
            for i in range(k + 1):
                ads = []
                for j in range(n):
                    vertex = ten2x(i, n, 1) + ten2x(j, n, 1)
                    ads.append(vertex)
                adss.append(ads)
        if k >= 2:
            adss = []
            kk = k - 1
            ver_add = LBCube_switch(n, kk).switch
            for i in range(k + 1):
                ads = []
                for j in range(n):
                    for ii in range(len(ver_add[0])):
                        ver = ver_add[0][ii][1:]
                        v_d = ten2x(i, n, 1) + ten2x(j, n, 1) + ver
                        ads.append(v_d)
                adss.append(ads)

        return adss


if __name__ == '__main__':
    # n = 5
    # kn = Kn(5)
    # print(kn.edges)


    LBCube_n_1(4)
    LBCube_n_k(5, 3)
    LBCube_switch(4, 2)
