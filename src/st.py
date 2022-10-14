import argparse
from tree import Node, linkedNode
import parser as p


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix tree")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()

    fasta = p.parseFasta(args.genome)
    fastq = p.parseFastq(args.reads)
    for (fastaName, fastaSeq) in fasta:
        for (name,seq) in fastq:
            for i in searchNaive(fastaSeq, seq):
                print(name, fastaName, i+1, f'{len(seq)}M', seq, sep="\t")



def constructTreeMcCreight(x: str, verbose=False):
    x += "$"
    n = len(x)

    firstLeaf = linkedNode((1, n), 0)
    root = linkedNode((0,0), {x[0] : firstLeaf})
    root.parent = root.suffixLink = root
    firstLeaf.parent = root
    lastHead = root
    
    if verbose:
        print("Going into loop with root", root.prettyString(), sep="\n")

    def fastScan(node: linkedNode, stringRange, suffixStart, suffixIndex, verbose) -> linkedNode:
        edgeStart, edgeEnd = stringRange
        if verbose:
            print("fastScan node", node.prettyString(), sep="\n")
            print("with z=", x[edgeStart-1:edgeEnd], sep="")
        if edgeStart <= 1:
            edgeStart = 1
        else:
            edgeStart -= 1
        index = edgeStart
        char = x[index]
        while index < edgeEnd:
            char = x[index]
            node = node.childrenOrLabel[char]
            index += 1
            l1, l2 = node.stringRange
            index += l2-l1
        if index > edgeEnd:
            if verbose:
                print("Need to split on the edge to node", node.prettyString(), sep="\n")
            newLeaf = linkedNode((suffixIndex+1, n), suffixStart)
            l1, l2 = node.stringRange
            splitNode = linkedNode((l1,edgeEnd), {x[suffixIndex] : newLeaf, x[edgeEnd] : node}, node.parent)
            newLeaf.parent = splitNode
            node.stringRange = (edgeEnd+1, l2)
            node.parent.childrenOrLabel[char] = splitNode
            node.parent = splitNode
            if verbose:
                print("fastScan returns the splitnode", splitNode.prettyString(), sep="\n")
                print("root after fastScan", root.prettyString(), sep="\n")

            return splitNode, True

        if verbose:
            print("fastScan returns the node", node.prettyString(), sep="\n")
        return node, False

    
    suffixIndex = 1
    for suffixStart in range(1, n):
        madeNewNode = False
        if verbose:
            print("Run with suffixStart", suffixStart, "and string", x[suffixStart:])
            print("SuffixIndex before", suffixIndex)
        if lastHead.parent == root:
            node = root
            suffixIndex = suffixStart
            char = x[suffixIndex]
            if char in node.childrenOrLabel:
                checknode = node.childrenOrLabel[char]
                a, b = checknode.stringRange
                if a==b:
                    node = checknode
                    suffixIndex += 1
            else:
                #new leaf
                newLeaf = linkedNode((suffixIndex+1, n), suffixStart, root)
                root.childrenOrLabel[char] = newLeaf
                node = root
            lastHead.suffixLink = node 
        else: 
            if verbose:
                print("lastHead", lastHead.prettyString(), sep="\n")
                print("parent", lastHead.parent.prettyString(), sep="\n")
                print("link", lastHead.parent.suffixLink.prettyString(), sep="\n")
            node, madeNewNode = fastScan(lastHead.parent.suffixLink, lastHead.stringRange, suffixStart, suffixIndex, verbose)
            lastHead.suffixLink = node 
            _, end = node.stringRange
            suffixIndex = end
            if madeNewNode:
                lastHead = node
                continue
        if suffixIndex==n:
            continue
        char = x[suffixIndex]

        while True:
            edgestart, edgeend = node.stringRange
            # prevSuffixIndex = suffixIndex
            
            i = 0
            for i in range(min(edgeend-edgestart, n-suffixIndex+1)):
                if suffixIndex == edgestart+i:
                    raise ValueError
                if x[suffixIndex] != x[edgestart+i]:
                    # Split node 
                    newLeaf = linkedNode((suffixIndex+1, n), suffixStart)
                    splitNode = linkedNode((edgestart,edgestart+i), {x[suffixIndex] : newLeaf, x[edgestart+i] : node}, node.parent)
                    newLeaf.parent = splitNode             
                    node.stringRange = (edgestart+i+1, edgeend)
                    node.parent.childrenOrLabel[char] = splitNode
                    node.parent = splitNode
                    lastHead = splitNode
                    if verbose:
                        print("Insert leaf by mismatch. Root is", root.prettyString(), sep="\n")
                    print("break")
                    break
                suffixIndex += 1 
            else: #Did not mismatch
                #FIXME should not happen
                # if suffixIndex == n: 
                #     # insert leaf with $       
                #     if i == edgeend-edgestart: #Did go all the way in edge
                #         if node.isInnerNode():
                #             newLeaf = linkedNode((n, n), suffixStart)
                #             newLeaf.parent = node
                #             node.childrenOrLabel["$"] = newLeaf
                #             lastHead = node
                #         else:
                #             raise ValueError
                #     else: #Stopped on an edge
                #         splitNode = linkedNode((suffixIndex, suffixIndex), {"$" : newLeaf, x[edgestart] : node}, node.parent)
                #         node.stringRange = (edgestart-1, edgeend)
                #         node.parent = splitNode
                #         lastHead = splitNode
                #         print(lastHead.prettyString())

                #     suffixIndex = prevSuffixIndex
                #     break
                char = x[suffixIndex]
                if verbose:
                    print("Got char", char)
                if char in node.childrenOrLabel:
                    suffixIndex += 1
                    node = node.childrenOrLabel[char]
                    if verbose:
                        print("Follow child to node", node.prettyString(), sep="\n")
                else: #Add new leaf to inner node
                    if verbose:
                        print("New leaf")
                    newLeaf = linkedNode((suffixIndex+1, n), suffixStart, node)
                    node.childrenOrLabel[char] = newLeaf
                    if verbose:
                        print("Add leaf to inner node", "Tree is now", root.prettyString(), sep="\n")
                    break
                continue
            break
    if verbose:
        print("Return tree", root.prettyString(), sep="\n")
    return root

def constructTreeNaive(x: str, verbose=False):
    x += "$"
    n = len(x)
    if verbose:
        print("x:", x)

    firstLeaf = Node((1, n), 0)
    root = Node((0,0), {x[0] : firstLeaf})
    root.parent = root
    firstLeaf.parent = root

    for suffixStart in range(1, n):
        node = root
        suffixIndex = suffixStart
        char = x[suffixIndex]

        while True:
            if verbose:
                print("Current root:\n", root.prettyString(), "\n")
                print("Current subtree:\n", node.prettyString())
                print("suffixIndex:", suffixIndex)
            edgestart, edgeend = node.stringRange
                
            for i in range(min(edgeend-edgestart, n-suffixIndex+1)):
                if verbose:
                    print("i", i)
                if x[suffixIndex] != x[edgestart+i]:
                    if verbose:
                        print("Mismatch")
                    # Split node 
                    newLeaf = Node((suffixIndex+1, n), suffixStart)
                    splitNode = Node((edgestart,edgestart+i), {x[suffixIndex] : newLeaf, x[edgestart+i] : node}, node.parent)
                    newLeaf.parent = splitNode             
                    node.stringRange = (edgestart+i+1, edgeend)
                    node.parent.childrenOrLabel[char] = splitNode
                    node.parent = splitNode
                    break
                suffixIndex += 1 
            else: #Did not mismatch
                if suffixIndex == n:
                    if verbose:
                        print("Got to n-1")
                    # insert leaf with $       
                    newLeaf = Node((n, n), suffixStart)
                    if node.isInnerNode():
                        newLeaf.parent = node
                        node.childrenOrLabel["$"] = newLeaf
                    else: 
                        splitNode = Node((suffixIndex, suffixIndex), {"$" : newLeaf, x[edgestart] : node}, node.parent)
                        node.stringRange = (edgestart-1, edgeend)
                        node.parent = splitNode
                    break

                char = x[suffixIndex]
                if node.isInnerNode():
                    if verbose:
                        print("Inner node")
                    if char in node.childrenOrLabel:
                        if verbose:
                            print("Follow child")
                        suffixIndex += 1
                        node = node.childrenOrLabel[char]
                    else: #Add new leaf to inner node
                        newLeaf = Node((suffixIndex+1, n), suffixStart, node)
                        node.childrenOrLabel[char] = newLeaf
                        break
                else:
                    if verbose:
                        print("Is leaf")
                    raise ValueError 
                continue
            break
    if verbose:
        print("Returning tree:\n", root.prettyString(), "\n")
    return root

def search(x, p):
    if not x or not p:
        return 
    t = constructTreeMcCreight(x)
    yield from searchTree(t, p, x+"$")

def searchNaive(x, p):
    if not x or not p:
        return 
    t = constructTreeNaive(x)
    yield from searchTree(t, p, x+"$")

def searchTree(tree: Node, p: str, x: str):
    node = tree
    # find pattern node
    i = 0
    m = len(p)
    while True:
        if i == m:
            yield from findLeaves(node)
            return
        if node.isLeaf():
            return 
        if not p[i] in node.childrenOrLabel:
            return
        node = node.childrenOrLabel[p[i]]
        i += 1 
        
        edgeStart, edgeEnd = node.stringRange
        for edgeIndex in range(edgeStart, edgeEnd):
            if i == m:
                yield from findLeaves(node)
                return
            if p[i] != x[edgeIndex]:
                return
            i += 1

def findLeaves(t: Node | None):
    stack = []
    if t:
        stack.append(t)
    
    while stack:
        node = stack.pop()
        if node.isLeaf():
            yield node.childrenOrLabel
        else:
            for c in node.childrenOrLabel.values():
                stack.append(c)

if __name__ == '__main__':
    main()