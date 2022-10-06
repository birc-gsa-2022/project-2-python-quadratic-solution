
from dataclasses import dataclass, field


@dataclass
class Node:
    children: dict[str, 'Node'] | None #TODO combine with label 
    stringRange: tuple[int, int] #Including first, excluding last
    label: int
    parent: 'Node | None' = field(default=None, compare=False) #Avoid recursive compareson. Not comparing parent is only a problem in special cases that should never happen

    # def __eq__(self, node):
    #     if node is None:
    #         return False
    #     if node.label != self.label:
    #         return False
    #     if node.stringRange != self.stringRange:
    #         return False
    #     if (node.parent is node) != (self.parent is self):
    #         return False
    #     # if node.children is None and self.children is None:
    #     #     return True
    #     # if node.children is None or self.children is None:
    #     #     return False
    #     return node.children == self.children