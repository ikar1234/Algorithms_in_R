# both Node() and Node should return True; the method should not be used with other classes
def isnone(cls) -> bool:
    if not isinstance(cls, Node):
        return True
    return cls.val is None


class Node:

    def __init__(self, val=None, parent=None, left=None, right=None,index=-1):
        # TODO: self.left resp. self.right should be a (named)tuple with the node and the corresponding string
        # TODO: use the indices of the LCP to get the suffixes from pos and the labeling of the edges
        self.val = val
        # return whole node
        self.parent = parent
        self.left = left
        # edges labeled with substrings, pointing to the children of the node
        self.leftedge = () # / None
        self.rightedge = ()
        self.right = right
        # store multiple keys in a linked list
        self.lbrother = None
        self.rbrother = None
        # used for the tree traversal
        self.visited = False
        # points to the corresponding index in the LCP-lcpay; we'll need it when making the final suffix tree
        self.index = index

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

    def get_leaf(self, right=True) -> int:
        """Returns one of the leaves under some edge. For speed reasons, this leaf will always be
        the leftmost one(LCP lcpay cannot be descending)."""
        if right:
            child = self.right
            while not isnone(child.left):
                child = child.left
        else:
            child = self.left
            while not isnone(child.left):
                child = child.left
        return child.val

    # needed to know whether the current node is also the root
    def __eq__(self, other):
        return self.val == other.val and self.right == other.right and self.left == other.left


class CartesianTree:
    """
    Approach to implement Cartesian trees, defined as follows:
    We aim to build a heap from given sequence
    Given an lcp array, the minimum/minima/ is at the top and all elements left from it
    are in the left subtree, respectively for the right.
    Linear time construction: Process the sequence from left to right, and proceed as follows:
    if the current element is bigger than the last one, put it as a right child, else go up in the tree
    until you find an element which is smaller than the current element.
    """
    """
    Implementation details:
    We need a pointer to the current node that we are processing;
    further we need to have backtraces. i.e. to be able to go from child to parent. 
    """
    def __init__(self, lcp):
        self.lcp = lcp
        if len(lcp) == 0:
            self.root = Node()
        else:
            self.root = Node(val=lcp[0], parent=Node(), left=Node(), right=Node())
        # make root active node
        self.active_node = self.root
        self.root.index = 0

        for x in range(1, len(lcp)):
            # find next smaller node and make it active
            while self.active_node != self.root and self.active_node.val > lcp[x]:
                self.active_node = self.active_node.parent
            if self.active_node == self.root:
                if self.active_node.val > lcp[x]:
                    # make the root left child of the new node
                    next_node = Node(val=lcp[x], parent=Node(), left=self.root, right=Node(), index=x)
                    self.root = next_node
                    self.active_node = next_node
                    # print(f"New root created: {self.root.val}")
                # handle special case with multiple keys in node
                elif self.active_node.val == lcp[x]:
                    next_node = Node(val=lcp[x], parent=Node(), left=self.active_node.right, right=Node(), index=x)
                    self.active_node.rbrother = next_node
                    next_node.lbrother = self.active_node
                    self.active_node = next_node
                else:
                    # put new node as a right child, possibly between two nodes
                    next_node = Node(val=lcp[x], parent=self.active_node,
                                     left=self.active_node.right, right=Node(), index=x)
                    self.active_node.right = next_node
                    self.active_node = next_node

            else:
                # multiple keys
                if self.active_node.val == lcp[x]:
                    next_node = Node(val=lcp[x], parent=self.active_node.parent,
                                     left=self.active_node.right, right=Node(), index=x)
                    self.active_node.rbrother = next_node
                    next_node.lbrother = self.active_node
                    self.active_node = next_node
                else:
                    # insert new node between two nodes
                    next_node = Node(val=lcp[x], parent=self.active_node, left=self.active_node.right,
                                     right=Node(), index=x)
                    self.active_node.right.parent = next_node
                    self.active_node.right = next_node
                    self.active_node = next_node

    def get_root(self):
        curr_node = self.root
        root_list = []
        while not isnone(curr_node.rbrother):
            root_list.append(self.root.rbrother)
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
                    # as we are assuming that we will go to him via his left brother
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
                curr_node.leftedge = (pos[0],len(pos))
                curr_node.left = Node(val=pos[c])
                c += 1
            elif isnone(curr_node.left):
                # this shouldn't happen
                assert False
            # we are at a leaf of the original tree
            if isnone(curr_node.right):
                # print('Right None',curr_node.val, c, iter)
                curr_node.visited = True
                # last node goes to the end of the string
                curr_node.rightedge = (pos[curr_node.index+1]+curr_node.val,len(pos))  # curr_node.get_leaf(right=True)
                curr_node.right = Node(val=pos[c])
                if not isnone(curr_node.rbrother):
                    curr_node.rbrother.left = curr_node.right
                c+=1
            else:
                # go to right (non-leaf) child
                curr_node.visited = True
                # the value curr_node.val corresponds to the lcp of pos[c] and pos[c-1]
                curr_node.rightedge = (curr_node.get_leaf(right=True) + curr_node.val,
                                       curr_node.get_leaf(right=True) + curr_node.right.val-1)
                curr_node = curr_node.right

            # assert not isnone(curr_node)
            # iter+=1


# string = ababa$
ct = CartesianTree(lcp=[0,1,3,0,2])
ct.decorate(pos=[6,5,3,1,4,2])
r = ct.get_root()
print(r[1].right.rightedge)   # 1 or 3 depending on whether we find leftmost or rightmost
