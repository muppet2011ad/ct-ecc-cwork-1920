def multMatrix(mat1, mat2):
    if len(mat1[0]) != len(mat2):
        return []
    result = [[0 for j in range(len(mat2[0]))] for i in range(len(mat1))]
    for i in range(len(mat1)):
        for j in range(len(mat2[0])):
            for k in range(len(mat2)):
                result[i][j] += mat1[i][k] * mat2[k][j]
    return result

def decimalToVector(i, l):
    vect = []
    while len(vect) < l:
        if i % 2 == 0:
            vect.append(0)
        else:
            vect.append(1)
        i = i // 2
    return vect[::-1]

def repetitionEncoder(m, n):
    return m * n


def repetitionDecoder(v):
    votes_0 = 0
    votes_1 = 0
    for bit in v:
        if bit == 0:
            votes_0 += 1
        else:
            votes_1 += 1
    if votes_0 > votes_1:
        return [0]
    elif votes_0 < votes_1:
        return [1]
    else:
        return []

# function HammingG
# input: a number r
# output: G, the generator matrix of the (2^r-1,2^r-r-1) Hamming code
def hammingGeneratorMatrix(r):
    n = 2 ** r - 1

    # construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2 ** (r - i - 1))
    for j in range(1, r):
        for k in range(2 ** j + 1, 2 ** (j + 1)):
            pi.append(k)

    # construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i + 1))

    # construct H'
    H = []
    for i in range(r, n):
        H.append(decimalToVector(pi[i], r))

    # construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n - r):
        GG.append(decimalToVector(2 ** (n - r - i - 1), n - r))

    # apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    # transpose
    G = [list(i) for i in zip(*G)]

    return G


def message(a):
    r = 2
    while 2 ** r - 2 * r - 1 < len(a):
        r += 1
    k = 2 ** r - r - 1
    body = decimalToVector(len(a), r) + a
    padding = (k - len(body)) * [0]
    return body + padding


def hammingEncoder(m):
    # Find r
    r = 2
    while 2 ** r - r - 1 != len(m):
        if len(m) < 2 ** r - r - 1:
            return []
        r += 1
    # Get generator matrix
    G = hammingGeneratorMatrix(r)
    # Multiply matrices to get encoded message
    c = multMatrix([m], G)
    return c[0]


def hammingDecoder(a):
    pass


def messageFromCodeword(a):
    pass


def dataFromMessage(a):
    pass
