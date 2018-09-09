def binary(n, bits=None):
    rem = []
    # divide by 2 and store the remainders
    while n != 0:
        rem.append(str(n%2))
        n/=2

    # if bit size is specified.
    if bits != None:
        while len(rem) != bits and len(rem) < bits:
            rem.append('0')
    return ''.join(rem[-1:-len(rem)-1:-1])

def decimal(binary_num):
    # self explanatory.
    binary_num = str(binary_num)
    binary_num = binary_num[-1:-len(binary_num)-1:-1]
    s = 0
    for i in range(len(binary_num)):
        s += (2**i)*int(binary_num[i])
    return s
    
def two_complement(binary_num):
    comp = ''
    binary_num = str(binary_num)
    for i in binary_num:
        if i == '1':
            comp+='0'
        else:
            comp += '1'
    # change the 1's complement number into decimal and add 1. Then return the binary.
    new = decimal(comp) + 1
    return binary(new)

def expand_two_comp_to(two_complement_number, bits):
    # take the sign bit of the 2's complement no. and replicate it in the front, till the bit size is achieved.
    sign_bit = two_complement_number[0]
    if bits > len(two_complement_number):
        while len(two_complement_number) < bits:
            two_complement_number = sign_bit+two_complement_number
    return two_complement_number

def expand(binary_number, bits):
    # add zeros in front till the bit size is achieved.
    while len(binary_number) != bits:
        binary_number  = '0'+binary_number
    return binary_number

def logical_shift_left(A, Q):
    # self explanatory.
    a0 = A[0]
    A = A[1:]
    A = A + Q[0]
    Q = Q[1:]
    Q = Q + a0
    return A, Q

def TableGen(n1, n2, bits):
    if n1 < 0:
        # example -14 in bits = 4
        # b1 = binary(14) = 1110
        # b1 = 2'sComp(b1=0111) = 0001+1=0010=10 will be the output
        # expand to bits = 0010
        # expand the complement with sign bit. Eg: 1011 to 8 bit will be 1111 1011 = 11111011
        b1 = binary(abs(n1), bits)
        b1 = two_complement(b1)
        b1 = expand(b1, bits)
        b1 = expand_two_comp_to(b1, bits)
    else:
        b1 = binary(n1, bits)
    if n2 < 0:
        b2 = two_complement(binary(abs(n2), bits))
        b2 = expand(b2, bits)
        b2 = expand_two_comp_to(b2, bits)
    else:
        b2 = binary(n2, bits)

    # expand b1 to 2*n bits.
    AQ = expand_two_comp_to(b1, 2*bits)
    A = AQ[0:bits]
    Q = AQ[bits:]
    return A, Q, b2, bits

def add(A, M, bits):
    A = decimal(A)
    M = decimal(M)
    A = A+M
    A = binary(A, bits)

    A = A[-1:-bits-1:-1]
    # ignore carry, if any.
    return A[-1:-len(A)-1:-1]

def subtract(A, M, bits):
    M = two_complement(M)
    M = expand(M, bits)
    return add(A, M, bits)

def inverse_two_complement(two_complement_no):
    d = decimal(two_complement_no) - 1
    d = binary(d)

    comp = ''

    for i in d:
        if i == '0':
            comp += '1'
        else:
            comp += '0'
    return comp

def division_algorithm(n1, n2, bits):
    A, Q, M, count = TableGen(n1, n2, bits)
    dividend = Q
    divisor = M
    print('Order: A Q M Count INSTRUCTION')
    print('{} {} {} {}'.format(A, Q, M, count))

    while count != 0:
        A, Q = logical_shift_left(A, Q)
        print('{} {} {} {} {}'.format(A, Q, M, count, 'LSL A, Q'))
        sign_A = A[0]
        original_A = A

        if A[0] == M[0]:
            A = subtract(A, M, bits)
            print('{} {} {} {} {}'.format(A, Q, M, count, 'A <--- A - M'))
        else:
            A = add(A, M, bits)
            print('{} {} {} {} {}'.format(A, Q, M, count, 'A <--- A + M'))

        if sign_A == A[0]:
            Q = Q[0:len(Q)-1]+'1'
            print('{} {} {} {} {}'.format(A, Q, M, count, 'Qo <--- 1'))
        else:
            Q = Q[0:len(Q)-1]+'0'
            A = original_A
            print('{} {} {} {} {}'.format(A, Q, M, count, 'Qo <--- 0 and RESTORE A'))
        
        count -= 1
        print('{} {} {} {} {}'.format(A, Q, M, count, 'Count <--- Count - 1'))

    if dividend[0] != divisor[0]:
        Q = two_complement(Q)

    if Q[0] == '1':
        q = inverse_two_complement(Q[1:])
        q = '-' + str(decimal(q))
    else:
        q = decimal(Q)
    if A[0] == '1':
        r = inverse_two_complement(A[1:])
        r = '-'+str(decimal(r))
    else:
        r = decimal(A)
    return 'Quotient: {} ({}), Remainder: {} ({})'.format(Q, q, A, r)
