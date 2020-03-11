def multMatrix(mat1, mat2):  # Takes two matrices and multiplies them (in binary)
    if len(mat1[0]) != len(mat2):  # If the dimensions don't match up for multiplication
        raise ValueError  # Throw an error
    result = [[0 for j in range(len(mat2[0]))] for i in range(len(mat1))]  # Initialise a results matrix of the proper dimensions
    for i in range(len(mat1)):  # For every row of mat1
        for j in range(len(mat2[0])):  # For every column of mat2
            for k in range(len(mat2)):  # For every row of mat2
                result[i][j] += mat1[i][k] * mat2[k][j]  # Perform the appropriate multiplication and add it to the cell
                if result[i][j] == 2:  # If we've added more than 1
                    result[i][j] = 0  # Wrap around to 0 since we're binary
    return result  # Return the result


def transposeMatrix(mat):  # Returns the transpose of a matrix
    return [[mat[i][j] for i in range(len(mat))] for j in range(len(mat[0]))]  # List comprehension constructs matrix rows from columns of input


def getHT(r):  # Gets matrix H transposed (it's actually easier to get the transpose rather than get the original H and transpose it)
    k = 2 ** r - 1  # Work out what k ought to be
    return [decimalToVector(i, r) for i in range(1, k + 1)]  # Construct a matrix with rows of the binary numbers 1 to k


def vectorToDecimal(v):  # Takes a binary vector and converts it to the decimal representation
    total = 0  # The total of our summation is 0
    for i in range(len(v)):  # For every digit in the vector
        total += v[::-1][i] * 2 ** i  # Increment the total by the value of that place
    return total  # Return the total


def decimalToVector(i, l):  # Takes a decimal number and converts it to its vector representation
    vect = []  # Construct an empty list for the vector
    while len(vect) < l:  # Whilst the vector we have is too short
        if i % 2 == 0:  # If i modulo 2 is zero
            vect.append(0)  # Append 0
        else:
            vect.append(1)  # Otherwise append 1
        i = i // 2  # Divided i by 2 and round down
    return vect[::-1]  # Flip the order of the vector to get the LSB on the right


def repetitionEncoder(m, n):  # Function to encode vector digit by repetition
    return m * n  # Duplicates the vector


def repetitionDecoder(v):  # Function to decode repetition encoded vector
    votes_0 = 0
    votes_1 = 0  # Tracks the number of bits that are 0 and 1
    for bit in v:  # For every bit increment the appropriate vote counter
        if bit == 0:
            votes_0 += 1
        else:
            votes_1 += 1
    if votes_0 > votes_1:  # If we have a majority for 0
        return [0]  # Return 0
    elif votes_0 < votes_1:  # If we have a majority for 1
        return [1]  # Return 1
    else:
        return []  # Otherwise it's unclear what we should have so we can't decode it

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


def message(a):  # Function converts vector to message format
    r = 2  # Find r
    while 2 ** r - 2 * r - 1 < len(a):
        r += 1
    k = 2 ** r - r - 1
    body = decimalToVector(len(a), r) + a  # The main body of the message is the length of the message followed by the message
    padding = (k - len(body)) * [0]  # We then have to pad zeroes to the full length
    return body + padding  # Return the combination of these vectors


def hammingEncoder(m):  # Encodes message to a hamming code
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


def hammingDecoder(v):  # Performs ECC to get original codeword
    r = 2  # Find r
    while 2 ** r - 1 != len(v):
        if len(v) < 2 ** r - 1:
            return []
        r += 1
    HT = getHT(r)  # Get the parity-check matrix H transposed
    col_i = multMatrix([v], HT)[0]  # Multiply our vector by the matrix to see if it's a valid codeword
    i = vectorToDecimal(col_i) - 1  # Convert the result to decimal so that it's easier to work with
    if i == -1:  # If it's a valid codeword
        return v  # Return it
    v[i] += 1  # Otherwise increment the corresponding position in the vector
    if v[i] == 2:
        v[i] = 0  # Wrap around to 0 where appropriate
    return v  # Return the new codeword (which should be a valid hamming code)


def messageFromCodeword(c):  # Gets message from hamming codeword
    r = 2  # Find r
    while 2 ** r - 1 != len(c):
        if len(c) < 2 ** r - 1:
            return []
        r += 1
    toRemove = [2 ** i - 1 for i in range(r)]  # Work out all of the powers of 2 we need to not include (except counting from 0 instead of 1)
    m = [c[i] for i in range(len(c)) if i not in toRemove]  # Remove these entries from the vector
    return m  # Return the message


def dataFromMessage(m):  # Gets data from the message
    r = 2  # Find r
    while 2 ** r - r - 1 != len(m):
        if len(m) < 2 ** r - 1:
            return []
        r += 1
    l = vectorToDecimal(m[:r])  # Gets the length of the data from the first r elements of the vector
    if l > len(m) - r:  # If the length given is longer than the rest of the vector then it's not valid
        return []  # So return the empty list
    a = m[r:r + l]  # Our data is the next l bits so we grab those
    return a  # And return them
