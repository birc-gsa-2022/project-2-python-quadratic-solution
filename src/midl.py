from tree import linkedNode


def constructTreeMcCreight(x: str, verbose=False):
    x += "$"
    n = len(x)

    firstLeaf = linkedNode((1, n), 0)
    root = linkedNode((0,0), {x[0] : firstLeaf})
    root.parent = root.suffixLink = root
    firstLeaf.parent = root
    lastHead = root
    
    def fastScan(node: linkedNode, stringRange: tuple[int, int], suffixStart: int, suffixIndex: int) -> tuple[linkedNode, bool]:
        fastEdgeStart, fastEdgeEnd = stringRange
        while True:
            if fastEdgeStart-1 == fastEdgeEnd:
                return node, False
            char = x[fastEdgeStart-1]
            node = node.childrenOrLabel[char]
            l1, l2 = node.stringRange
            curEdgeLen = l2-l1
            nextFastEdgeStart = fastEdgeStart+curEdgeLen+1 
            if nextFastEdgeStart-1 > fastEdgeEnd: 
                #split on this edge
                newLeaf = linkedNode((suffixIndex+1, n), suffixStart)

                splitIndex = l1 + fastEdgeEnd - fastEdgeStart
                splitNode = linkedNode((l1,splitIndex), {x[suffixIndex] : newLeaf, x[splitIndex] : node}, node.parent)
                newLeaf.parent = splitNode
                node.stringRange = (splitIndex+1, l2)
                node.parent.childrenOrLabel[char] = splitNode
                node.parent = splitNode

                return splitNode, True
            fastEdgeStart = nextFastEdgeStart

    suffixIndex = 1
    for suffixStart in range(1, n):
        madeNewNode = False
        if lastHead == root:
            node = root
            suffixIndex = suffixStart
        else:
            hstart, hend = lastHead.stringRange
            node, madeNewNode = fastScan(lastHead.parent.suffixLink, (hstart+(lastHead.parent == root), hend), suffixStart, suffixIndex)
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
            continue
                
        while True:
            edgestart, edgeend = node.stringRange
            
            i = 0
            for i in range(edgeend-edgestart):
                if x[suffixIndex] != x[edgestart+i]:
                    # Split node 
                    newLeaf = linkedNode((suffixIndex+1, n), suffixStart)
                    splitNode = linkedNode((edgestart,edgestart+i), {x[suffixIndex] : newLeaf, x[edgestart+i] : node}, node.parent)
                    newLeaf.parent = splitNode             
                    node.stringRange = (edgestart+i+1, edgeend)
                    node.parent.childrenOrLabel[char] = splitNode
                    node.parent = splitNode
                    lastHead = splitNode
                    break
                suffixIndex += 1 
            else: #Did not mismatch
                char = x[suffixIndex]
                if char in node.childrenOrLabel:
                    suffixIndex += 1
                    node = node.childrenOrLabel[char]
                else: #Add new leaf to inner node
                    newLeaf = linkedNode((suffixIndex+1, n), suffixStart, node)
                    node.childrenOrLabel[char] = newLeaf
                    lastHead = node
                    break
                continue
            break
    return root


#print(constructTreeMcCreight("gccgcgcc", True).prettyString())
#print(constructTreeMcCreight("ababbab", True).prettyString())
#print(constructTreeMcCreight("cttccc", True).prettyString())
