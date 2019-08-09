# both Node() and Node should return True; the method should not be used with other classes
def isnone(cls) -> bool:
    if not isinstance(cls, Node):
        return True
    return cls.val is None


class Node:

    def __init__(self, val=None, parent=None, left=None, right=None, leaf=False):
        self.val = val
        # return whole node
        self.parent = parent
        self.left = left
        self.right = right
        # store multiple keys in a linked list
        self.lbrother = None
        self.rbrother = None
        # value of the SA are stored in the leaves
        self.leaf = leaf
        # needed for the tree traversal
        self.visited = False

    def left(self):
        curr_node = self.left
        l = []
        while curr_node.lbrother is not None:
            l.append(self.left().lbrother)
            curr_node = curr_node.lbrother
        return [self.left()] + l

    def get_right(self):
        # returns the whole list of keys, not only the first key
        curr_node = self.right
        r = []
        while curr_node.rbrother is not None:
            r.append(self.right.rbrother)
            curr_node = curr_node.rbrother
        return [self.right] + r

    def rec_print(self):
        if self is None:
            return ''
        l = self.left
        r = self.right
        print(str(self.val), '[ ', end='')
        if l is not None:
            l.rec_print()
        else:
            print('-', end='')
        if r is not None:
            r.rec_print()
        else:
            print('-', end='')
        print(' ]', end='')

    # both Node() and None should return True

    # needed to know whether the current node is also the root
    def __eq__(self, other):
        return self.val == other.val and self.right == other.right and self.left == other.left


class CartesianTree:
    """
    Desperate approach to implement Cartesian trees, defined as follows:
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
    def __init__(self, arr):
        self.arr = arr
        if len(arr) == 0:
            self.root = Node()
        else:
            self.root = Node(val=arr[0], parent=Node(), left=Node(), right=Node())
        # make root active node
        self.active_node = self.root

        for x in range(1, len(arr)):
            # find next smaller node and make it active
            while self.active_node != self.root and self.active_node.val > arr[x]:
                self.active_node = self.active_node.parent
            if self.active_node == self.root:
                if self.active_node.val > arr[x]:
                    # make the root left child of the new node
                    next_node = Node(val=arr[x], parent=Node(), left=self.root, right=Node())
                    self.root = next_node
                    self.active_node = next_node
                    # print(f"New root created: {self.root.val}")
                # handle special case with multiple keys in node
                elif self.active_node.val == arr[x]:
                    next_node = Node(val=arr[x], parent=Node(), left=self.active_node.right, right=Node())
                    self.active_node.rbrother = next_node
                    next_node.lbrother = self.active_node
                    self.active_node = next_node
                else:
                    # put new node as a right child, possibly between two nodes
                    next_node = Node(val=arr[x], parent=self.active_node, left=self.active_node.right, right=Node())
                    self.active_node.right = next_node
                    self.active_node = next_node

            else:
                # multiple keys
                if self.active_node.val == arr[x]:
                    next_node = Node(val=arr[x], parent=self.active_node.parent,
                                     left=self.active_node.right, right=Node())
                    self.active_node.rbrother = next_node
                    next_node.lbrother = self.active_node
                    self.active_node = next_node
                else:
                    # insert new node between two nodes
                    next_node = Node(val=arr[x], parent=self.active_node, left=self.active_node.right, right=Node())
                    self.active_node.right.parent = next_node
                    self.active_node.right = next_node
                    self.active_node = next_node

    def get_root(self):
        curr_node = self.root
        root_list = []
        while not isnone(curr_node.rbrother):
            r.append(self.root.rbrother)
            curr_node = curr_node.rbrother
        return [self.root]+root_list

    def decorate(self, pos) -> None:
        """
        Add the SA-entries to the leaves of the tree.
        Assumes that SA contains dollar sign at position 1.
        Uses an in-order traversal of the tree to assign each None-pointer a value from the SA.
        """
        root = self.get_root()
        curr_node = root[0]
        # dollar sign is always left child of first root key
        c = 0
        # iter = 0
        while True:
            # print('Generic;',curr_node.val,c,iter)
            # only break condition
            if c >= len(pos):
                break
            if curr_node.visited:
                # print('Visited;',curr_node.val, c,iter)
                if isnone(curr_node.rbrother) and not isnone(curr_node.parent):
                    # last key in node, so go to the parent node
                    # every time we go back to the first key in the parent, and still can find the right key,
                    # since all keys up to this key are marked as visited
                    curr_node.visited = True
                    curr_node = curr_node.parent
                    # print('Go to father', curr_node.val, c, iter)
                else:
                    # print('Go to brother;', curr_node.val, c, iter)
                    curr_node.visited = True
                    # assert not isnone(curr_node.rbrother)
                    curr_node = curr_node.rbrother
                # iter+=1
                continue
            # if we are in a node with multiple keys, the right child of the one key is the left of the second
            # => if key has left brothers, don't go to left child
            if isnone(curr_node.left) and isnone(curr_node.lbrother):
                # print('Left child is None, leftmost mode',curr_node.val, c, iter)
                curr_node.visited = True
                curr_node.left = Node(val=pos[c], leaf=True)
                c += 1
            elif isnone(curr_node.left):
                # print('Left is None and middle node',curr_node.val, c, iter)
                curr_node.visited = True
                curr_node = curr_node.left
                # iter+=1
                continue
            # we are at a leaf of the original tree
            if isnone(curr_node.right):
                # print('Right None',curr_node.val, c, iter)
                curr_node.visited = True
                curr_node.right = Node(val=pos[c], leaf=True)
                if not isnone(curr_node.rbrother):
                    curr_node.rbrother.left = curr_node.right
                c+=1
            else:
                curr_node.visited = True
                curr_node = curr_node.right
            # assert not isnone(curr_node)
            # iter+=1


# string = aaaaa$ -> exclude first 0; SA = 6,5,4,3,2,1
ct = CartesianTree([0,0,2,3,4])
ct.decorate([10,20,30,40,50,60])
r = ct.get_root()
# print(r[1].right.right.left.val)
r[0].rec_print()
