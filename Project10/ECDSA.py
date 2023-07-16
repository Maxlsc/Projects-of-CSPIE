import secrets

def QR(n, p):
    return pow(n, (p - 1) // 2, p)

def solveQR(n, p):
    assert QR(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if QR(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r

def invese(B, N):
    if B == N:
        return (B, 1, 0)
    else:
        i = 0
        b = [B]
        n = [N]
        q = []
        r = []
        flag = False

        while not flag:
            q.append(n[i] // b[i])
            r.append(n[i] % b[i])
            n.append(b[i])
            b.append(r[i])
            if r[i] == 0:
                flag = True
            i += 1
        tmp = b[i - 1]
        x = [1]
        y = [0]

        i -= 2;
        num = i

        while i >= 0:
            y.append(x[num - i])
            x.append(y[num - i] - q[i] * x[num - i])
            i -= 1

        return (tmp, x[-1], y[-1])


def xgcd(b, n):
    (g, x, y) = invese(b, n)

    if g == 1:
        return x % n
    else:
        return -1


a = 0
b = 7
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (x, y)

def add(P, Q): 
    if P == 0 and Q == 0:
        return 0
    elif P == 0:
        return Q
    elif Q == 0:
        return P
    else:
        if P[0] > Q[0]:
            tmp = P
            P = Q
            Q = tmp

        Z = []
        t = (Q[1] - P[1]) * xgcd(Q[0] - P[0], p) % p
        Z.append((t ** 2 - P[0] - Q[0]) % p)
        Z.append((t * (P[0] - Z[0]) - P[1]) % p)
        return (Z[0], Z[1])


def epoint_add1(P):  
    Z = []
    tmp = (3 * P[0] ** 2 + a) * xgcd(2 * P[1], p) % p
    Z.append((tmp ** 2 - 2 * P[0]) % p)
    Z.append((tmp * (P[0] - Z[0]) - P[1]) % p)
    return (Z[0], Z[1])


def multi(k, g):
    tmp = g
    z = 0
    k_bin = bin(k)[2:]
    k_len = len(k_bin)

    for i in reversed(range(k_len)):
        if k_bin[i] == '1':
            z = add(z, tmp)
        tmp = epoint_add1(tmp)

    return z


def keygen():
    sk = int(secrets.token_hex(32), 16)
    pk = multi(sk, G)
    return sk, pk



def signature(sk, m):
    e = hash(m)
    k = secrets.randbelow(p)  
    R = multi(k, G) 
    r = R[0] % p
    s = xgcd(k, n) * (e + r * sk) % n

    return (r, s)  # 

def deduce(sign, m):
    r = sign[0]
    s = sign[1]
    x = r % p
    y = solveQR(((x ** 3) + 7), p)
    e = hash(m)

    P1 = (x, y)
    P2 = (x, p - y)
    sk1 = multi(s % n, P1)
    tmp = multi(e % n, G)
    tmp_i = (tmp[0], p - tmp[1])
    tmp_1 = add(sk1, tmp_i)
    pk1 = multi(xgcd(r, n), tmp_1)

    sk2 = multi(s % n, P2)
    tmp_2 = add(sk2, tmp_i)
    pk2 = multi(xgcd(r, n), tmp_2)
    return pk1, pk2


if __name__ == '__main__':
    sk, pk = keygen()
    print("Public Key: \n", pk)
    m = "this is message"
    s = signature(sk, m)
    print("\nSignature:\n ", s)
    pub1, pub2 = deduce(s, m)
    print('\nPossible 1：\n', pub1)
    print('\nPossible 2：\n', pub2)
    if pub1==pk:
      print('\np1 is pk\n')
    if pub2==pk:
     print('\np2 is pk\n')
