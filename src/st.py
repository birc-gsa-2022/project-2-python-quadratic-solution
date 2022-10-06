import argparse
from tree import Node


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix tree")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()
    print(f"Find every reads in {args.reads.name} " +
          f"in genome {args.genome.name}")



# Index does not work
# Don't mind all the broken code 
def constructTreeNaive(x: str):
    x += "$"
    n = len(x)

    firstLeaf = Node(None, (1, n), 0)
    root = Node({x[0] : firstLeaf}, (0,0), 0)
    root.parent = root
    firstLeaf.parent = root

    for i in range(1, n):
        node = root
        char = x[i]
        if char in node.children:
            node = node.children[char]
            start, end = node.stringRange
            for j in range(min(end-start+1, n-i-1)):
                print("j", j)
                print("j+start", j+start)
                print("j+i", j+i)
                stringPos = j+i+1
                treePos = j+start
                if x[treePos] != x[stringPos]: #TODO find which to use for mismatch
                    splitNode = Node(None, stringRange=(start, stringPos), label=node.label, parent=node.parent)
                    newChild = Node(None, stringRange=(stringPos, n), label=i, parent=splitNode)
                    splitNode.children = {x[treePos]: node, x[stringPos]: newChild}
                    node.stringRange = (stringPos, end)
                    node.parent.children[char] = splitNode
                    #print("splitnode", splitNode)
                    print("================================================")
        else:
            newChild = Node(None, (i+1, n), i, node)
            node.children[char] = newChild

    return root
        
ct = constructTreeNaive("aa")
print("lab", ct.label)
print(ct)
print("==========================")
print(ct.children["a"].stringRange)

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

