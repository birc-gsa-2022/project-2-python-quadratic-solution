import argparse
from re import T
from tree import Node


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix tree")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()
    print(f"Find every reads in {args.reads.name} " +
          f"in genome {args.genome.name}")



def isInnerNode(node: Node):
    return node.children is not None

def constructTreeNaive(x: str, verbose=False):
    x += "$"
    n = len(x)
    if verbose:
        print("x:", x)

    firstLeaf = Node(None, (1, n), 0)
    root = Node({x[0] : firstLeaf}, (0,0), None)
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
                    newLeaf = Node(None, (suffixIndex+1, n), suffixStart)
                    splitNode = Node({x[suffixIndex] : newLeaf, x[edgestart+i] : node}, (edgestart,edgestart+i), None, node.parent)
                    newLeaf.parent = splitNode             
                    node.stringRange = (edgestart+i+1, edgeend)
                    node.parent.children[char] = splitNode
                    node.parent = splitNode
                    break
                suffixIndex += 1 
            else: #Did not mismatch
                if suffixIndex == n:
                    if verbose:
                        print("Got to n-1")
                    # insert leaf with $       
                    newLeaf = Node(None, (n, n), suffixStart)
                    if isInnerNode(node):
                        newLeaf.parent = node
                        node.children["$"] = newLeaf
                    else: 
                        splitNode = Node({"$" : newLeaf, x[edgestart] : node}, (suffixIndex, suffixIndex), None, node.parent)
                        node.stringRange = (edgestart-1, edgeend)
                        node.parent = splitNode
                    break

                char = x[suffixIndex]
                if isInnerNode(node):
                    if verbose:
                        print("Inner node")
                    if char in node.children:
                        if verbose:
                            print("Follow child")
                        suffixIndex += 1
                        node = node.children[char]
                    else: #Add new leaf to inner node
                        newLeaf = Node(None, (suffixIndex+1, n), suffixStart, node)
                        node.children[char] = newLeaf
                        break
                else: # split leaf 
                    if verbose:
                        print("Is leaf")

                    raise NotImplementedError 
                    break
                continue
            break
    if verbose:
        print("Returning tree:\n", root.prettyString(), "\n")
    return root
        


    # for i in range(1, n):
    #     node = root
    #     char = x[i]
    #     if char in node.children:
    #         node = node.children[char]
    #         start, end = node.stringRange
    #         for j in range(min(end-start+1, n-i-1)):
    #             print("j", j)
    #             print("j+start", j+start)
    #             print("j+i", j+i)
    #             stringPos = j+i+1
    #             treePos = j+start
    #             if x[treePos] != x[stringPos]: #TODO find which to use for mismatch
    #                 splitNode = Node(None, stringRange=(start, stringPos), label=node.label, parent=node.parent)
    #                 newChild = Node(None, stringRange=(stringPos, n), label=i, parent=splitNode)
    #                 splitNode.children = {x[treePos]: node, x[stringPos]: newChild}
    #                 node.stringRange = (stringPos, end)
    #                 node.parent.children[char] = splitNode
    #                 #print("splitnode", splitNode)
    #                 print("================================================")
    #     else:
    #         newChild = Node(None, (i+1, n), i, node)
    #         node.children[char] = newChild


# def constructTreeNaive(x: str):
#     x += "$"
#     n = len(x)
#     root = Node({}, (0,0), 0)
#     root.parent = root
#     for i in range(n):
#         print("i", i)
#         node = root
#         print("node", node)
#         char = x[i]
#         strI = i
#         while True:
#             start, end = node.stringRange
#             for j in range(end-start): #Compare to substring on edge
#                 print("j", j)
#                 strI = j+strI
#                 char = x[strI]
#                 if char != x[start+j]: #Mismatch on edge
#                     print("mismatch")
#                     splitNode = Node(None, stringRange=(start, strI), label=i, parent=node.parent)
#                     newChild = Node(None, stringRange=(strI, n), label=i, parent=splitNode)
#                     splitNode.children = {x[start+j]: node, char: newChild}
#                     node.stringRange = (j, end)
#                     node.parent.children[char] = splitNode
#                     break #Stop comparing edge
#             else: #Go to next (child) node
#                 if node.children is None:
#                     print("\n \n")
#                     print("root", root)
#                     print("node", node)
#                     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaah")
#                     print("\n \n")
#                 elif char in node.children:
#                     node = node.children[char]
#                     continue
#                 else: #Can not follow children
#                     newChild = Node(None, (strI+1, n), i, parent=node)
#                     node.children[char] = newChild
#                     break # Suffix has been inserted. Go to next suffix.
            
            
#             break # Suffix has been inserted. Go to next suffix. 

#     return root

# def constructTreeNaive(x: str):
#     x += "$"
#     n = len(x)
#     root = Node({}, (0,0), 0)
#     root.parent = root
#     for i in range(n):
#         print("i", i)
#         node = root
#         print("node", node)
#         char = x[i]
#         while node.children and char in node.children: #While can go deeper 
#             start, end = node.stringRange
#             for j in range(end-start): #Compare to substring on edge
#                 print("j", j)
#                 strI = j+i
#                 char = x[strI]
#                 if char != x[start+j]: #Mismatch on edge
#                     print("mismatch")
#                     splitNode = Node(stringRange=(start, strI))
#                     newChild = Node(stringRange=(strI, n))
#                     splitNode.children = {x[start+j]: node, char: newChild}

#                     node.stringRange = (j, end)
#                     node.parent.children[char] = splitNode #TODO try update if not works 
#                     break #Stop compoaring edge
#             else: #Go to next (child) node
#                 node = node.children[char]
#                 continue
#             break # Suffix has been inserted. Go to next suffix. 
#         else: #Could not go deeper 
#             print("nodeChild", node.children)
#             newChild = Node(None, (i+1, n), label=i, parent=node)
#             # if not node.children: #TODO make sure this is not broken, if we change to use children memory for label
#             #     start, end = node.stringRange
#             #     splitNode = Node({x[start]: node, char : newNode}, (start))
#             try:
#                 node.children[char] = newChild
#             except:
#                 print("pass")

#     return root


# if __name__ == '__main__':
#     main()

