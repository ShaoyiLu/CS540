import sys
import string
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)


def shred(filename):
    # Using a dictionary here. You may change this to any data structure of
    # your choice such as lists (X=[]) etc. for the assignment
    X = dict()
    with open(filename, encoding='utf-8') as f:
        X = dict.fromkeys(string.ascii_uppercase, 0)
        for line in f:
            word_string = line.upper()
            word_string = word_string.replace(' ', '')
            for char in word_string:
                if char.isalpha():
                    X[char] += 1
    return X


def other_calculation(filename):
    X = shred(filename)
    Y = get_parameter_vectors()

    print('Q2')
    # print(Y[0]) is a list of e
    print('{:.4f}'.format(X['A'] * math.log(Y[0][0])))
    print('{:.4f}'.format(X['A'] * math.log(Y[1][0])))

    add_English = 0
    ei_English = 0
    for char in X:
        add_English += X[char] * math.log(Y[0][ei_English])
        ei_English += 1

    total_English = add_English + math.log(0.6)

    add_Spanish = 0
    si_Spanish = 0
    for char in X:
        add_Spanish += X[char] * math.log(Y[1][si_Spanish])
        si_Spanish += 1

    total_Spanish = add_Spanish + math.log(0.4)

    print('Q3')
    print('{:.4f}'.format(total_English))
    print('{:.4f}'.format(total_Spanish))

    print('Q4')
    Z = total_Spanish - total_English
    if Z >= 100:
        PYEnglish = 0
        print(PYEnglish)
    elif Z <= -100:
        PYEnglish = 1
        print(PYEnglish)
    else:
        PYEnglish = '{:.4}'.format(1 / (1 + pow(math.e, Z)))
        print(PYEnglish)

def main():
    print('Q1')
    X = shred('letter.txt')
    for key, value in X.items():
        print(key, value)

    other_calculation('letter.txt')


if __name__ == "__main__":
    main()