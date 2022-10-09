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