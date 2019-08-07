
class Node:

    def __init__(self,val=None,parent=None,left=None,right=None):
        self.val = val
        self.parent = parent
        self.left = left
        self.right = right

    def set_val(self,val):
        self.val = val

    @property
    def get_val(self):
        return self.val

    def __str__(self):
        """Print subtree. If you want to print only the value, use print(Node.val)"""
        return f'{self.val} [{print(self.left)},{self.right}]'

    # needed to know whether the current node is also the root
    def __eq__(self, other):
        return self.val == other.val and self.right==other.right and self.left==other.left


class CartesianTree(): # inherit from binary tree?
    """
    Approach to implement Cartesian trees, defined as follows:
    We aim to build a heap from given sequence
    Given an array, the minimum/minima/ is at the top and all elements left from it
    are in the left subtree, respectively for the right.
    Linear time construction: Process the sequence from left to right, and proceed as follows:
    if the current element is bigger than the last one, put it as a right child, else go up in the tree
    until you find an element which is smaller than the current element.
    """
    """
    Implementation details:
    We need a pointer to the current node that we are processing;
    further we need to have backtraces. i.e. to be able to go from child to parent 
    """
    def __init__(self,arr):
        self.arr = arr
        if len(arr)==0:
            self.root=Node()
        else:
            self.root = Node(val=arr[0],parent=Node(),left=Node(),right=Node())
        # make root active node
        self.active_node = self.root

        for x in range(1,len(arr)):
            # find next smaller node and make it active
            while self.active_node!=self.root and self.active_node.val > arr[x]:
                self.active_node = self.active_node.parent
            if self.active_node==self.root:
                # want to insert a node as a right child or between 2 nodes
                if self.active_node.val > arr[x]:
                    # make the root left child of the new node
                    next_node = Node(val=arr[x], parent=Node(), left=self.root, right=Node())
                    self.root = next_node
                    self.active_node = next_node
                    # print(f"New root created: {self.root.val}")
                else:
                    # put new node as a right child, possibly between two nodes
                    next_node = Node(val=arr[x], parent=self.active_node, left=self.active_node.right, right=Node())
                    self.root.right = next_node
                    self.active_node = next_node

            else:
                # insert new node between two nodes
                next_node = Node(val=arr[x], parent=self.active_node, left=self.active_node.right, right=Node())
                self.active_node.right.parent = next_node
                self.active_node.right = next_node
                self.active_node = next_node

    def get_root(self):
        return self.root


ct = CartesianTree([6,9,2,4,7,8,5,8,3,7])

# print tree for every permutation of 10 elements
r = ct.get_root()
print('\t\t',r.val)
print('\t',r.left.val,end='\t\t')
print('\t',r.right.val)
print(r.left.left.val,end='\t\t')
print(r.left.right.val,end='\t')
print(r.right.left.val,end='\t\t')
print(r.right.right.val)


