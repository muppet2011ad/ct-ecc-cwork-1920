def decimalToVector(i, l):
    binary = bin(i)
    binarray = [int(x) for x in binary[2:]]
    padding = [0] * (l - len(binarray))
    return padding + binarray


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
    pass


def hammingEncoder(a):
    pass


def hammingDecoder(a):
    pass


def messageFromCodeword(a):
    pass


def dataFromMessage(a):
    pass
