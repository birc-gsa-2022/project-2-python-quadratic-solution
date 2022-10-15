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

    def fastScan(node: linkedNode, stringRange: tuple[int, int], suffixStart: int, suffixIndex: int) -> linkedNode:
        edgeStart, edgeEnd = stringRange
        if verbose:
            print("fastScan node", node.prettyString(), sep="\n")
            print("with z=", x[edgeStart-1:edgeEnd], sep="")
        if edgeStart <= 1: #TODO needed? 
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
            sameBranch = node==lastHead
            l1, l2 = node.stringRange
            assert x[suffixIndex] != x[edgeEnd-sameBranch], f"Added same symbol, {x[edgeEnd]}, with index {suffixIndex} and {edgeEnd}"
            splitNode = linkedNode((l1,edgeEnd-sameBranch), {x[suffixIndex] : newLeaf, x[edgeEnd-sameBranch] : node}, node.parent)
            newLeaf.parent = splitNode
            node.stringRange = (edgeEnd+(not sameBranch), l2)
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
        while True:
            edgestart, edgeend = node.stringRange
            
            i = 0
            for i in range(edgeend-edgestart):
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
                assert node.isInnerNode(), "Is leaf"
                assert suffixIndex != n, f"suffixIndex=n for y={x[suffixStart:]} and x={x}"
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

#print(constructTreeMcCreight("mississippi", True).prettyString())
#print(constructTreeMcCreight("cttccc", True).prettyString())
