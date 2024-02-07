import numpy as np

# Converts the number n in decimal to X and represents it as a string
def ten2x(n, x, l): # n: a decimal number    x: x-bit    l: the length of string
    a = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V']
    b = []
    while True:
        s = n // x
        y = n % x
        b = b + [y]
        if s == 0:
            break
        n = s
    nt = []
    for i in b:
        nt.append(a[i])
    for i in range(l-len(nt)):
        nt.append('0')
    nt.reverse()
    return "".join(nt)


# Physical structure: switches, servers, and wires
class BCube_n_k():
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.server = self.servers(n, k)
        self.switch = self.switches(n, k)
        self.wire = self.wires(n, k)

    def servers(self, n, k):
        if k == 1:
            address_s = []   # record the address of each server
            for i in range(n):
                v = []
                for j in range(n):
                    vertex = ten2x(i, n, 1) + ten2x(j, n, 1) + 'a'
                    v.append(vertex)
                address_s.append(v)
            return address_s
        else:
            v = []
            for i in range(n):   #  Based on BCube(n,1)
                x = []
                for j in range(n):
                    vertex = ten2x(i, n, 1) + ten2x(j, n, 1) + 'a'
                    x.append(vertex)
                v.append(x)
            for i in range(1, k):
                address_s = []
                for j in range(n):
                    u = []
                    for a in range(n):
                        for b in range(n * (n ** (i - 1))):
                            vertex = ten2x(j, n, 1) + v[a][b]
                            u.append(vertex)
                    address_s.append(u)
                v = address_s.copy()

            return address_s

    def switches(self, n, k):
        adss = []
        if k == 1:
            adss = []
            for i in range(k+1):
                ads = []
                for j in range(n):
                    vertex = ten2x(i, n, 1) + ten2x(j, n, 1) + 's'
                    ads.append(vertex)
                adss.append(ads)
        if k == 2:
            adss = []
            for i in range(k+1):
                ads = []
                for j in range(n):
                    ver = ten2x(i, n, 1) + ten2x(j, n, 1)
                    for ii in range(n):
                        v_d = ver + ten2x(ii, n, 1) + 's'
                        ads.append(v_d)
                adss.append(ads)

        if k == 3:
            adss = []
            for i in range(k + 1):
                ads = []
                for j in range(n):
                    ver = ten2x(i, n, 1) + ten2x(j, n, 1)
                    for ii in range(n):
                        v_d = ver + ten2x(ii, n, 1)
                        for jj in range(n):
                            v_g = v_d + ten2x(jj, n, 1) + 's'
                            ads.append(v_g)
                adss.append(ads)

        if k == 4:
            adss = []
            for i in range(k + 1):
                ads = []
                for j in range(n):
                    ver = ten2x(i, n, 1) + ten2x(j, n, 1)
                    for ii in range(n):
                        v_d = ver + ten2x(ii, n, 1)
                        for jj in range(n):
                            v_g = v_d + ten2x(jj, n, 1)
                            for jjj in range(n):
                                v_final = v_g + ten2x(jjj, n, 1) + 's'
                                ads.append(v_final)
                adss.append(ads)

        return adss

    def wires(self, n, k):
        a_server = self.server
        s_switch = self.switch
        links = []
        # Consider first the case k = 0
        links_0 = []
        a_server_copy = a_server.copy()
        a_server_array = np.array(a_server_copy)
        a_server_sum = list(a_server_array.flatten())
        for s in s_switch[0]:
            for i in range(n):
                a = a_server_sum[0]
                link = (a, s)
                links_0.append(link)
                a_server_sum.remove(a)
        links.append(links_0)

        # Consider the case k > 1
        for i in range(1, k+1):
            a_server_sum = list(a_server_array.flatten())
            link_i = []
            if i == k:
                for s_1 in range(len(s_switch[i])):
                    s = s_switch[i][s_1]
                    for j in range(n):
                        a = a_server_sum[j * (n ** i) + s_1]
                        link = (a, s)
                        link_i.append(link)
            else:
                for s_1 in range(len(s_switch[i])):
                    s = s_switch[i][s_1]
                    s_num = int(s_1 / (n ** i))
                    s_e = s_1 % (n ** i)
                    for j in range(n):
                        a = a_server_sum[j * (n ** i) + s_num * (n ** (i+1)) + s_e]
                        link = (a, s)
                        link_i.append(link)

            links.append(link_i)

        return links





if __name__ == '__main__':
    n = 4
    k = 2
    BCube_n_k(n, k)
