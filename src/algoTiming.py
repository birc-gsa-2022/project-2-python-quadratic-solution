import timer as t
import st
import random as r
import pandas as pd
import numpy as np
from playsound import playsound
  


timer = t.Clock()

# numIterations = 100
# numAvgIterations = 5
# maxSeqlen = 100000
# minSeqlen = 10000
# seqlenstep = 10000
# patlen1 = 1
# patlen2 = 10
# patlen3 = 100
alphabet = "acgt"


def timeVarN(name, numIterations, numAvgIterations, maxSeqlen, minSeqlen, seqlenstep, patlen1, patlen2, patlen3):
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
    data['Naive'] = lNaive
    data['McCreight'] = lMcCreight
    data['Search'+str(patlen1)] = lpat1
    data['Search'+str(patlen2)] = lpat2
    data['Search'+str(patlen3)] = lpat3

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f"{name}.csv", index=False)

def timeVarNShowAll(name, numIterations, numAvgIterations, maxSeqlen, minSeqlen, seqlenstep, patlen1, patlen2, patlen3):
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
        print("Seq len is now:", seqLen)
        
        for _ in range(numIterations):
            seq = "".join(r.choices(alphabet, k=seqLen))
            naive, tree = timer.getAverageTimeAndResult(numAvgIterations, st.constructTreeNaive, seq)
            lNaive.append(naive)

            seq = "".join(r.choices(alphabet, k=seqLen))
            mcCreight = timer.getAverageTime(numAvgIterations, st.constructTreeMcCreight, seq)
            lMcCreight.append(mcCreight)
        
            pat1 = "".join(r.choices(alphabet, k=patlen1)) 
            pat2 = "".join(r.choices(alphabet, k=patlen2))
            pat3 = "".join(r.choices(alphabet, k=patlen3))
            tPat1 = timer.getAverageTime(numAvgIterations, st.searchTree, tree, pat1, seq)
            tPat2 = timer.getAverageTime(numAvgIterations, st.searchTree, tree, pat2, seq)
            tPat3 = timer.getAverageTime(numAvgIterations, st.searchTree, tree, pat3, seq)
            lpat1.append(tPat1)
            lpat2.append(tPat2)
            lpat3.append(tPat3)

            lseq.append(seqLen)  

    data['n'] = lseq
    data['Naive'] = lNaive
    data['McCreight'] = lMcCreight
    data['Search'+str(patlen1)] = lpat1
    data['Search'+str(patlen2)] = lpat2
    data['Search'+str(patlen3)] = lpat3

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f"{name}.csv", index=False)

def timeBuildNaiveAndMcCreight(name, maxSeqLen, minSegLen, segLenStep, alphabet, numAvgIterations, saveTree=False):
    data = {"n": list(range(minSegLen, maxSeqLen, segLenStep))}
    lNaive = []
    lMcCreight = []
    if saveTree:
        trees = []
    for seqLen in range(minSegLen, maxSeqLen, segLenStep):
        print("Seq len is now:", seqLen)
        seq = "".join(r.choices(alphabet, k=seqLen))
        naiveTime = timer.getAverageTime(numAvgIterations, st.constructTreeNaive, seq)
        lNaive.append(naiveTime)

        seq = "".join(r.choices(alphabet, k=seqLen))
        mcTime, tree = timer.getAverageTimeAndResult(numAvgIterations, st.constructTreeMcCreight, seq)
        lMcCreight.append(mcTime)
        if saveTree:
            trees.append(tree)
    data["Naive"] = lNaive
    data["McCreight"] = lMcCreight

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f"{name}.csv", index=False)

    if saveTree:
        return trees, list(range(minSegLen, maxSeqLen, segLenStep))

def timeSearchVarM(name, maxM, minM, mStep, seqLens, alphabet, numAvgIterations):
    n1, n2, n3 = seqLens
    seq1 = "".join(r.choices(alphabet, k=n1))
    seq2 = "".join(r.choices(alphabet, k=n2))
    seq3 = "".join(r.choices(alphabet, k=n3))
    t1 = st.constructTreeMcCreight(seq1)
    t2 = st.constructTreeMcCreight(seq2)
    t3 = st.constructTreeMcCreight(seq3)

    data = {"m": list(range(minM, maxM, mStep))}
    s1Times = []
    s2Times = []
    s3Times = []
    
    for m in range(minM, maxM, mStep):
        print("m is now:", m)
        pat = "".join(r.choices(alphabet, k=m))
        s1Time = timer.getAverageTime(numAvgIterations, st.searchTree, t1, pat, seq1)
        s2Time = timer.getAverageTime(numAvgIterations, st.searchTree, t2, pat, seq2)
        s3Time = timer.getAverageTime(numAvgIterations, st.searchTree, t3, pat, seq3)
        s1Times.append(s1Time)
        s2Times.append(s2Time)
        s3Times.append(s3Time)
    
    data[f"n={n1}"] = s1Times
    data[f"n={n2}"] = s2Times
    data[f"n={n3}"] = s3Times

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f"{name}.csv", index=False)


def timeBuildNaiveAndMcCreightSameChar(name, maxSeqLen, minSegLen, segLenStep, numAvgIterations, saveTree=False):
    data = {"n": list(range(minSegLen, maxSeqLen, segLenStep))}
    lNaive = []
    lMcCreight = []
    if saveTree:
        trees = []
    for seqLen in range(minSegLen, maxSeqLen, segLenStep):
        print("Seq len is now:", seqLen)
        seq = "a"*seqLen
        naiveTime = timer.getAverageTime(numAvgIterations, st.constructTreeNaive, seq)
        lNaive.append(naiveTime)

        seq = "b"*seqLen
        mcTime, tree = timer.getAverageTimeAndResult(numAvgIterations, st.constructTreeMcCreight, seq)
        lMcCreight.append(mcTime)
        if saveTree:
            trees.append(tree)
    data["Naive"] = lNaive
    data["McCreight"] = lMcCreight

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f"{name}.csv", index=False)

    if saveTree:
        return trees, list(range(minSegLen, maxSeqLen, segLenStep))

def timeBuildMcCreight(name, maxSeqLen, minSegLen, segLenStep, alphabet, numAvgIterations, saveTree=False):
    data = {"n": list(range(minSegLen, maxSeqLen, segLenStep))}
    lMcCreight = []
    if saveTree:
        trees = []
    for seqLen in range(minSegLen, maxSeqLen, segLenStep):
        print("Seq len is now:", seqLen)
        seq = "".join(r.choices(alphabet, k=seqLen))
        mcTime, tree = timer.getAverageTimeAndResult(numAvgIterations, st.constructTreeMcCreight, seq)
        lMcCreight.append(mcTime)
        if saveTree:
            trees.append(tree)
    data["McCreight"] = lMcCreight

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f"{name}.csv", index=False)

    if saveTree:
        return trees, list(range(minSegLen, maxSeqLen, segLenStep))


def multiSearch(iterations, tree, pattern, x):
    for _ in range(iterations-1):
        st.searchTree(tree, pattern, x)
    return len(list(st.searchTree(tree, pattern, x)))


def timeSearchVarMExists(name, maxM, minM, mStep, seqLens, alphabet, numAvgIterations):
    n1, n2, n3 = seqLens
    seq1 = "".join(r.choices(alphabet, k=n1))
    seq2 = "".join(r.choices(alphabet, k=n2))
    seq3 = "".join(r.choices(alphabet, k=n3))
    t1 = st.constructTreeMcCreight(seq1)
    print("t1 made")
    t2 = st.constructTreeMcCreight(seq2)
    print("t2 made")
    t3 = st.constructTreeMcCreight(seq3)
    print("t3 made")

    data = {"m": list(range(minM, maxM, mStep))}
    s1Times = []
    s2Times = []
    s3Times = []
    s1Lens = []
    s2Lens = []
    s3Lens = []
    
    for m in range(minM, maxM, mStep):
        print("m is now:", m)
        index = r.randint(0, n1-m)
        pat = seq1[index:index+m]
        s1Time, res1 = timer.getAlgorithmTimeAndResult(multiSearch, 1, t1, pat, seq1)
        index = r.randint(0, n2-m)
        pat = seq2[index:index+m]
        s2Time, res2 = timer.getAlgorithmTimeAndResult(multiSearch, 1, t2, pat, seq2)
        index = r.randint(0, n3-m)
        pat = seq3[index:index+m]
        s3Time, res3 = timer.getAlgorithmTimeAndResult(multiSearch, 1, t3, pat, seq3)
        s1Times.append(s1Time)
        s2Times.append(s2Time)
        s3Times.append(s3Time)
        s1Lens.append(res1)
        s2Lens.append(res2)
        s3Lens.append(res3)
    
    data[f"n={n1}"] = s1Times
    data[f"n={n2}"] = s2Times
    data[f"n={n3}"] = s3Times
    data[f"Output len for n={n1}"] = s1Lens
    data[f"Output len for n={n2}"] = s2Lens
    data[f"Output len for n={n3}"] = s3Lens

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f"{name}.csv", index=False)

#timeSearchVarMExists("data11VarM", 10**5, 0, 1, (10**5, 10**6, 10**7), alphabet, 1)

#runTestVarN("data1")
#timeBuildMcCreight("data8sameChar", 10**6+1, 10**3, 10**3, "a", 1)
#timeSearchVarM("data6", 100000, 10, 10, (100000, 1000000, 10000000), alphabet, 1)
#timeVarNShowAll("data3", 1, 3, 10**6, 10**5, 10**5, 10, 100, 1000)
