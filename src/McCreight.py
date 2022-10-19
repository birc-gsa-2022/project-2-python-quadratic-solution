from tree import linkedNode


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

    def fastScan(node: linkedNode, stringRange: tuple[int, int], suffixStart: int, suffixIndex: int) -> tuple[linkedNode, bool]:
        fastEdgeStart, fastEdgeEnd = stringRange
        if verbose:
            print("fastScan node", node.prettyString(), sep="\n")
            print("fastEdgestart, fastEdgeEnd", fastEdgeStart, fastEdgeEnd) #3, 4
            print("with z=", x[fastEdgeStart-1:fastEdgeEnd], sep="")
        while True:
            if fastEdgeStart-1 == fastEdgeEnd:
                if verbose:
                    print("fastScaned to node", node.prettyString(), sep="\n")
                return node, False
            char = x[fastEdgeStart-1]
            assert char in node.childrenOrLabel, f"{char} was not in dictinary of node \n{node.prettyString()}\n for x={x}"
            node = node.childrenOrLabel[char]
            l1, l2 = node.stringRange
            curEdgeLen = l2-l1
            nextFastEdgeStart = fastEdgeStart+curEdgeLen+1
            if nextFastEdgeStart-1 > fastEdgeEnd:
                #split on this edge
                if verbose:
                    print("Need to split on the edge to node", node.prettyString(), sep="\n")
                newLeaf = linkedNode((suffixIndex+1, n), suffixStart)

                splitIndex = l1 + fastEdgeEnd - fastEdgeStart
                assert x[suffixIndex] != x[splitIndex], f"Added same symbol, {x[splitIndex]}, with index {suffixIndex} and {splitIndex} for x={x}"
                assert l1 <= splitIndex, f"About to make splitnode with impossible indecies {l1} and {splitIndex} for x={x}"
                splitNode = linkedNode((l1,splitIndex), {x[suffixIndex] : newLeaf, x[splitIndex] : node}, node.parent)
                newLeaf.parent = splitNode
                assert splitIndex <= l2, f"About to insert impossible indecies {splitIndex} and {l2} for x={x}"
                node.stringRange = (splitIndex+1, l2)
                node.parent.childrenOrLabel[char] = splitNode
                node.parent = splitNode
                if verbose:
                    print("fastScan returns the splitnode", splitNode.prettyString(), sep="\n")
                    print("root after fastScan", root.prettyString(), sep="\n")

                return splitNode, True
            fastEdgeStart = nextFastEdgeStart

    suffixIndex = 1
    for suffixStart in range(1, n):
        madeNewNode = False
        if verbose:
            print("================================================================")
            print("Run with suffixStart", suffixStart, ", suffixIndex", suffixIndex, ", and string", x[suffixStart:])
        if lastHead == root:
            if verbose:
                print("lastHead is root, continue with slow scan")
            node = root
            suffixIndex = suffixStart

        elif lastHead.parent == root:
            if verbose:
                print("lastHead.parent is root")
                print("lastHead", lastHead.prettyString(), sep="\n")
            hstart, hend = lastHead.stringRange
            node, madeNewNode = fastScan(root, (hstart+1, hend), suffixStart, suffixIndex)
            
            lastHead.suffixLink = node
            _, end = node.stringRange
            suffixIndex = max(end, suffixStart, suffixIndex)
            if verbose:
                print("Set suffix link of", lastHead.prettyString(), "when fast scanning I to", node.prettyString(), sep="\n")
                print("set suffixIndex to", suffixIndex)
                print("root is", root.prettyString(), sep="\n")
        else: 
            if verbose:
                print("lastHead", lastHead.prettyString(), sep="\n")
                print("parent", lastHead.parent.prettyString(), sep="\n")
                print("link", lastHead.parent.suffixLink.prettyString(), sep="\n")
            node, madeNewNode = fastScan(lastHead.parent.suffixLink, lastHead.stringRange, suffixStart, suffixIndex)
            if verbose:
                print("Set suffix link when fast scanning II to", node.prettyString(), sep="\n")
            lastHead.suffixLink = node 
            _, end = node.stringRange
            suffixIndex = max(end, suffixStart, suffixIndex)
        if madeNewNode:
            lastHead = node
            continue
        if suffixIndex==n:
            continue
        

        #Slow scan 
        char = x[suffixIndex] 

        if char not in node.childrenOrLabel:
            lastHead = node
            newLeaf = linkedNode((suffixIndex+1, n), suffixStart, node)
            node.childrenOrLabel[char] = newLeaf
            if verbose:
                print("Insert leaf  by char:", char)
                print("Root is now", root.prettyString(), sep="\n")
            continue
                
        while True:
            edgestart, edgeend = node.stringRange
            if verbose:
                print("edgestart and edgeend are", edgestart, edgeend)
                print("suffixindex is", suffixIndex)
            
            i = 0
            for i in range(edgeend-edgestart): #TODO: Is the fast scan node checked twice? 
                assert suffixIndex != edgestart+i, f"suffixIndex=edgestart+{i}={suffixIndex} for y={x[suffixStart:]} and x={x}"
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
                    break
                suffixIndex += 1 
            else: #Did not mismatch
                assert node.isInnerNode(), f"Leaf found when x={x}"
                assert suffixIndex != n, f"suffixIndex=n for y={x[suffixStart:]} and x={x}"
                char = x[suffixIndex]
                if verbose:
                    print("Got char", char)
                if char in node.childrenOrLabel:
                    suffixIndex += 1
                    if verbose:
                        print(f"Follow child {char} of node", node.prettyString(), sep="\n")
                        print("suffixIndex", suffixIndex)
                    node = node.childrenOrLabel[char]
                else: #Add new leaf to inner node
                    if verbose:
                        print("New leaf")
                    newLeaf = linkedNode((suffixIndex+1, n), suffixStart, node)
                    node.childrenOrLabel[char] = newLeaf
                    lastHead = node
                    if verbose:
                        print("Add leaf to inner node", "Tree is now", root.prettyString(), sep="\n")
                    break
                continue
            break
    if verbose:
        print("Return tree", root.prettyString(), sep="\n")
    return root


#print(constructTreeMcCreight("gccgcgcc", True).prettyString())

#print(constructTreeMcCreight("aaaa", True).prettyString())
#print(constructTreeMcCreight("ababbab", True).prettyString())
#print(constructTreeMcCreight("cttccc", True).prettyString())
