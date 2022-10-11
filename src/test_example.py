# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_
import st
from tree import Node


def test_constructTreeNaiveChildren():
    res = st.constructTreeNaive("")
    leafSen = Node(None, (1,1), 0)
    root = Node({"$" : leafSen}, (0,0), None)
    leafSen.parent = root
    root.parent = root
    assert res == root, "Not same tree for empty string"
    
    res = st.constructTreeNaive("a")
    leafA = Node(None, (1,2), 0)
    leafSen = Node(None, (2,2), 1)
    expT = Node({"a" : leafA, "$": leafSen}, (0,0), None)
    leafA.parent = expT
    leafSen.parent = expT
    expT.parent = expT
    assert res == expT, "Not same tree for a"

    res = st.constructTreeNaive("ab")
    leafAB = Node(None, (1,3), 0) 
    leafB = Node(None, (2,3), 1) 
    leafSen = Node(None, (3,3), 2) 
    leaves = {"a" : leafAB, "b" : leafB, "$" : leafSen}
    expT = Node(leaves, (0,0), None)
    assert res == expT, "Not same tree for ab"


def test_constructTreeNaiveSplit():
    res = st.constructTreeNaive("aa")
    leafAA = Node(None, (2,3), 0) 
    leafA = Node(None, (3,3), 1) 
    leafSen = Node(None, (3,3), 2) 
    nodeA = Node({"a": leafAA, "$" : leafA}, (1,1), None)
    root = Node({"a" : nodeA, "$": leafSen}, (0,0), None)

    leafAA.parent = leafA.parent = nodeA
    nodeA.parent = root
    root.parent = root

    assert res == root, "Not same tree for aa"

def test_search():
    res = list(st.search("a", "a"))
    assert res == [0], "Not correct for x=a and p=a"

    res = list(st.search("aaaaaa", "a"))
    res.sort()
    assert res == [0,1,2,3,4,5], "Not correct for x=aaaaaa and p=a"



def leafNotExists(y: str, tree: Node) -> bool:
    node = tree.children[y[0]]
    i = 1
    while True:
        #TODO make this
        break
    return False

def isValidTree(x: str, tree: Node) -> bool:
    x += "$"
    n = len(x)
    if tree.children is None:
        return False
    if not "$" in tree.children:
        return False
    if tree.children["$"].label != n:
        return False
    for i in range(n):
        if leafNotExists(x[i:], tree):
            return False
    return True






















# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_
import random as r
import lin 

genAlphabet = "acgt"

def setSeed(seed=None):
    if seed == None:
        seed = r.randint(0,1000)
    with open("seed.txt", "a") as f:
        f.write(f"Last seed was {seed} \n" )
    r.seed(seed)


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
    compare_res(x, p, st.search, lin.kmp2)

    x = "mississippi"
    p = "ssi" 
    compare_res(x, p, st.search, lin.kmp2)

    x = "aaaaa"
    p = "aa"
    compare_res(x, p, st.search, lin.kmp2)

    x = "gtccccacatcct"
    p = "ccc"
    compare_res(x, p, st.search, lin.kmp2)


def test_random_same():
    setSeed()
    for i in range(100):
        x= "".join(r.choices(genAlphabet, k=i))
        for j in range(50, i+2):
            pat = "".join(r.choices(genAlphabet, k=j))
            compare_res(x, pat, st.search, lin.kmp2)


def test_search():
    x = ["aaaaa", "mississippi","", "aaabc","abc","a b c", "abababbababa", "Genome", "abxabxabx", "abxabdabx", "bcagjkdasbca"]
    p = ["aa", "iss","","bc", "abcd", "b ", "ba", "good grades", "abc", "abx", "a"]
    expected = [[0,1,2,3],[1,4],[],[3],[],[2],[1,3,6,8,10], [], [],[0,6],[2,7,11]]

    for i in range(len(x)):
        res = list(st.search(x[i],p[i]))
        res.sort()
        assert res == expected[i]