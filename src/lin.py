"""Implementation of a linear time exact matching algorithm."""

import argparse
import parser as p


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching in linear time")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()
    
    fasta = p.parseFasta(args.genome)
    fastq = p.parseFastq(args.reads)
    for (fastaName, fastaSeq) in fasta:
        for (name,seq) in fastq:
            for i in kmp2(fastaSeq, seq):
                print(name, fastaName, i+1, f'{len(seq)}M', seq, sep="\t")


def border_array(x: str) -> list[int]:
    ba = []

    for i, char in enumerate(x):
        j = i 
        while True:
            if j == 0:
                ba.append(0)
                break
            baPrev = ba[j-1]
            if x[baPrev] == char:
                ba.append(baPrev+1)
                break
            j = baPrev 
    return ba

def strict_border_array(x: str, ba=None) -> list[int]:
    if ba is None:
        ba = border_array(x)
    for i, bai in enumerate(ba[:-1]):
        if bai != 0 and x[i+1] == x[bai]:
            ba[i]= ba[bai-1]  
    return ba

def kmp(x, p):
    if not x or not p:
        return 
    ba = border_array(p)
    bax = strict_border_array(p, ba.copy())
    m = len(p)
    n = len(x)
    i = 0
    j = 0
    while j < n:
        if x[j] == p[i]:
            if i==m-1:
                yield j-i
                j += (i == 0)
                i = ba[i-1]
            else:
                j += 1
                i += 1
        elif i==0:
            j += 1
        else:
            i = bax[i-1]

def kmp2(x, p):
    if not x or not p:
        return 
    bax = strict_border_array(p)
    m = len(p)
    n = len(x)
    j = 0

    matchLen = 0
    while j <= n-(m-matchLen):
        for i in range(matchLen, m):
            if x[j] == p[i]:
                matchLen += 1
                j +=1 
            else:
                break
        else:
            yield j-matchLen
        if matchLen == 0:
            j += 1
        else:
            matchLen = bax[matchLen-1]

def make_jump_table(p):
    jump_table = dict()
    m = len(p)
    # Only makes entry for letter there is in p
    for i in range(len(p)-1):
        jump_table[p[i]] = m - i - 1
    return jump_table

def bmh(x, p):
    if not x or not p:
        return 
    
    n = len(x)
    m = len(p)
    jump_table = make_jump_table(p)
    j = 0

    while j < n - m + 1:
        i = m - 1 # strings index's starts at 0
        while 0 <= i and p[i] == x[j + i]:
            i -= 1
        
        if i == -1:
            yield j
        
        j += jump_table.get(x[j+m-1], m)

if __name__ == '__main__':
    main()
