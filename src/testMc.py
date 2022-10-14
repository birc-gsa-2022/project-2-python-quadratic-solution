# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_
import st
from tree import Node, linkedNode
import random as r
import lin 

genAlphabet = "acgt"

def setSeed(seed=None):
    if seed == None:
        seed = r.randint(0,1000)
    with open("seed.txt", "a") as f:
        f.write(f"Last seed for search was {seed} \n" )
    r.seed(seed)

def leafExists(y: str, tree: Node, label: int, x: str) -> bool:
    node = tree.childrenOrLabel[y[0]]
    i = 1
    while node.isInnerNode():
        startEdge, endEdge = node.stringRange
        assert y[i:i+endEdge-startEdge] == x[startEdge:endEdge], f"{y[i:i+endEdge-startEdge]} != {x[startEdge:endEdge]}"
        i += endEdge-startEdge
        node = node.childrenOrLabel[y[i]]
        i += 1 
    startEdge, endEdge = node.stringRange
    assert y[i:i+endEdge-startEdge] == x[startEdge:endEdge], f"{y[i:i+endEdge-startEdge]} != {x[startEdge:endEdge]}, {y}[{i}:{i+endEdge-startEdge}] != {x}[{startEdge}:{endEdge}]"
    assert node.childrenOrLabel == label, f"Got label {node.childrenOrLabel}, not {label}"


def isValidTree(x: str, tree: Node) -> bool:
    x += "$"
    n = len(x)
    assert tree.isInnerNode(), f"Tree leaf x={x}"
    assert "$" in tree.childrenOrLabel, f"$ not leaf in tree for x={x}"
    assert tree.childrenOrLabel["$"].childrenOrLabel == n-1, f"$ have label {tree.childrenOrLabel['$'].childrenOrLabel}, not {n-1} for x={x}"
    for i in range(n):
        leafExists(x[i:], tree, i, x)
    return True


def test_constructTreeMcCreightChildren():
    res = st.constructTreeMcCreight("")
    leafSen = linkedNode((1,1), 0)
    root = linkedNode((0,0), {"$" : leafSen})
    leafSen.parent = root
    root.parent = root
    assert res == root, "Not same tree for empty string"
    
    res = st.constructTreeMcCreight("a")
    leafA = linkedNode((1,2), 0)
    leafSen = linkedNode((2,2), 1)
    expT = linkedNode((0,0), {"a" : leafA, "$": leafSen})
    leafA.parent = expT
    leafSen.parent = expT
    expT.parent = expT
    assert res == expT, f"Not same tree for a. Got \n{res.prettyString()} instead of \n{expT.prettyString()}"

    res = st.constructTreeMcCreight("ab")
    leafAB = linkedNode((1,3), 0) 
    leafB = linkedNode((2,3), 1) 
    leafSen = linkedNode((3,3), 2) 
    leaves = {"a" : leafAB, "b" : leafB, "$" : leafSen}
    expT = linkedNode((0,0), leaves)
    assert res == expT, f"Not same tree for ab. Got \n{res.prettyString()} instead of \n{expT.prettyString()}"

def test_constructTreeMcCreightSplit():
    res = st.constructTreeMcCreight("aa")
    leafAA = linkedNode((2,3), 0) 
    leafA = linkedNode((3,3), 1) 
    leafSen = linkedNode((3,3), 2) 
    nodeA = linkedNode((1,1), {"a": leafAA, "$" : leafA})
    root = linkedNode((0,0), {"a" : nodeA, "$": leafSen})

    leafAA.parent = leafA.parent = nodeA
    nodeA.parent = root
    root.parent = root

    assert res == root, "Not same tree for aa"



def test_random_valid_McCreight():
    setSeed()
    for i in range(500):
        x= "".join(r.choices(genAlphabet, k=i))
        t = st.constructTreeMcCreight(x)
        isValidTree(x, t)
        t2 = st.constructTreeNaive(x)
        t.assertEqualToNode(t2), f"Naive and McCreight gave different trees on string {x}. \n{t.prettyString()}\n{t2.prettyString()}"




def test_search():
    res = list(st.search("a", "a"))
    resNaive = list(st.searchNaive("a", "a"))
    assert res == [0], "Not correct for x=a and p=a"
    assert resNaive == [0], "Not correct for x=a and p=a"

    res = list(st.search("aaaaaa", "a"))
    res.sort()
    resNaive = list(st.searchNaive("aaaaaa", "a"))
    resNaive.sort()
    assert res == [0,1,2,3,4,5], "Not correct for x=aaaaaa and p=a"
    assert resNaive == [0,1,2,3,4,5], "Not correct for x=aaaaaa and p=a"




def compare_res(x, p, *algorithms):
    res = [list(a(x,p)) for a in algorithms]
    res.sort()
    for i in range(1, len(res)):
        assert len(res[0]) == len(res[i]), f"Not same len for {algorithms[0].__name__} and {algorithms[i].__name__} with input {x} and {p}"
    for i in range(1, len(res)):
        assert res[0] == res[i], f"Not same output for {algorithms[0].__name__()} and {algorithms[i].__name__()} with input {x} and {p}"

def test_defined():
    x = ""
    p = ""
    compare_res(x, p, st.search, st.searchNaive, lin.kmp2)

    x = "mississippi"
    p = "ssi" 
    compare_res(x, p, st.search, st.searchNaive, lin.kmp2)

    x = "aaaaa"
    p = "aa"
    compare_res(x, p, st.search, st.searchNaive, lin.kmp2)

    x = "gtccccacatcct"
    p = "ccc"
    compare_res(x, p, st.search, st.searchNaive, lin.kmp2)


def test_random_same():
    setSeed()
    for i in range(100):
        x= "".join(r.choices(genAlphabet, k=i))
        for j in range(50, i+2):
            pat = "".join(r.choices(genAlphabet, k=j))
            compare_res(x, pat, st.search, st.searchNaive, lin.kmp2)

def test_search():
    x = ["aaaaa", "mississippi","", "aaabc","abc","a b c", "abababbababa", "Genome", "abxabxabx", "abxabdabx", "bcagjkdasbca"]
    p = ["aa", "iss","","bc", "abcd", "b ", "ba", "good grades", "abc", "abx", "a"]
    expected = [[0,1,2,3],[1,4],[],[3],[],[2],[1,3,6,8,10], [], [],[0,6],[2,7,11]]

    for i in range(len(x)):
        resMc = list(st.search(x[i],p[i]))
        resMc.sort()
        resNaive = list(st.searchNaive(x[i],p[i]))
        resNaive.sort()
        assert resMc == expected[i]
        assert resMc == resNaive
