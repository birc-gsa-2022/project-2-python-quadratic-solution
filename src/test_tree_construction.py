# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_
import st
from tree import Node
import random as r

def test_constructTreeNaiveChildren():
    res = st.constructTreeNaive("")
    leafSen = Node((1,1), 0)
    root = Node((0,0), {"$" : leafSen})
    leafSen.parent = root
    root.parent = root
    assert res == root, "Not same tree for empty string"
    
    res = st.constructTreeNaive("a")
    leafA = Node((1,2), 0)
    leafSen = Node((2,2), 1)
    expT = Node((0,0), {"a" : leafA, "$": leafSen})
    leafA.parent = expT
    leafSen.parent = expT
    expT.parent = expT
    assert res == expT, "Not same tree for a"

    res = st.constructTreeNaive("ab")
    leafAB = Node((1,3), 0) 
    leafB = Node((2,3), 1) 
    leafSen = Node((3,3), 2) 
    leaves = {"a" : leafAB, "b" : leafB, "$" : leafSen}
    expT = Node((0,0), leaves)
    assert res == expT, "Not same tree for ab"


def test_constructTreeNaiveSplit():
    res = st.constructTreeNaive("aa")
    leafAA = Node((2,3), 0) 
    leafA = Node((3,3), 1) 
    leafSen = Node((3,3), 2) 
    nodeA = Node((1,1), {"a": leafAA, "$" : leafA})
    root = Node((0,0), {"a" : nodeA, "$": leafSen})

    leafAA.parent = leafA.parent = nodeA
    nodeA.parent = root
    root.parent = root

    assert res == root, "Not same tree for aa"


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
    assert y[i:i+endEdge-startEdge] == x[startEdge:endEdge], f"{y[i:i+endEdge-startEdge]} != {x[startEdge:endEdge]}"
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

def setSeed(seed=None):
    if seed == None:
        seed = r.randint(0,1000)
    with open("seed.txt", "a") as f:
        f.write(f"Last seed for construction was {seed} \n" )
    r.seed(seed)

genAlphabet = "acgt" 

def test_random_valid():
    setSeed()
    for i in range(100):
        x= "".join(r.choices(genAlphabet, k=i))
        t = st.constructTreeNaive(x)
        isValidTree(x, t)