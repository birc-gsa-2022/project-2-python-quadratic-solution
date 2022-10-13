import timer as t
import st
import random as r
import pandas as pd
import numpy as np

timer = t.Clock()
numIterations = 100
numAvgIterations = 5
alphabet = "acgt"
maxSeqlen = 10000
minSeqlen = 1000
seqlenstep = 1000
patlen1 = 1
patlen2 = 10
patlen3 = 100


def runTestVarN():
    data = dict()

    lseq = []
    lpat1 = []
    lpat2 = []
    lpat3 = []

    lNaive = []
    lMcCreight = []

    #We generate a new seqeunce to look through before a run of an algorithm 
    #This is done to minizime the amout knowlegde python has of the seqence before running each algorithm  

    for seqLen in range(minSeqlen, maxSeqlen+1, seqlenstep):
        print("Seq len is now:",seqLen)
        tempNaive = []
        tempMcCreight = []
        tempPat1 = []
        tempPat2 = []
        tempPat3 = []
        
        for _ in range(numIterations):
            seq = "".join(r.choices(alphabet, k=seqLen))
            naive, tree = timer.getAverageTimeAndResult(numAvgIterations, st.constructTreeNaive, seq)
            tempNaive.append(naive)

            seq = "".join(r.choices(alphabet, k=seqLen))
            mcCreight = timer.getAverageTime(numAvgIterations, st.constructTreeMcCreight, seq)
            tempMcCreight.append(mcCreight)
        
            pat1 = "".join(r.choices(alphabet, k=patlen1)) 
            pat2 = "".join(r.choices(alphabet, k=patlen2))
            pat3 = "".join(r.choices(alphabet, k=patlen3))
            tPat1 = timer.getAverageTime(numAvgIterations, st.searchTree, tree, pat1, seq)
            tPat2 = timer.getAverageTime(numAvgIterations, st.searchTree, tree, pat2, seq)
            tPat3 = timer.getAverageTime(numAvgIterations, st.searchTree, tree, pat3, seq)
            tempPat1.append(tPat1)
            tempPat2.append(tPat2)
            tempPat3.append(tPat3)

        lseq.append(seqLen)  
        lNaive.append(np.average(tempNaive))
        lMcCreight.append(np.average(tempMcCreight))
        lpat1.append(np.average(tempPat1))
        lpat2.append(np.average(tempPat2))
        lpat3.append(np.average(tempPat3))

    data['n'] = lseq
    data['naive'] = lNaive
    data['McCreight'] = lMcCreight
    data['Search'+str(patlen1)] = lpat1
    data['Search'+str(patlen2)] = lpat2
    data['Search'+str(patlen3)] = lpat3

    dataframe = pd.DataFrame(data)
    dataframe.to_csv("data1.csv", index=False)
