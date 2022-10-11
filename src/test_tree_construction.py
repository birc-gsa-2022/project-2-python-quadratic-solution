# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_
import st
from tree import Node
import random as r

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


def leafExists(y: str, tree: Node, label: int, x: str) -> bool:
    node = tree.children[y[0]]
    i = 1
    while node.isInnerNode():
        startEdge, endEdge = node.stringRange
        assert y[i:i+endEdge-startEdge] == x[startEdge:endEdge], f"{y[i:i+endEdge-startEdge]} != {x[startEdge:endEdge]}"
        i += endEdge-startEdge
        node = node.children[y[i]]
        i += 1 
    startEdge, endEdge = node.stringRange
    assert y[i:i+endEdge-startEdge] == x[startEdge:endEdge], f"{y[i:i+endEdge-startEdge]} != {x[startEdge:endEdge]}"
    assert node.label == label, f"Got label {node.label}, not {label}"

def isValidTree(x: str, tree: Node) -> bool:
    x += "$"
    n = len(x)
    assert tree.children is not None, f"Tree is none for x={x}"
    assert "$" in tree.children, f"$ not leaf in tree for x={x}"
    assert tree.children["$"].label == n-1, f"$ have label {tree.children['$'].label}, not {n-1} for x={x}"
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