########################################################
##### IMPLEMENTATION OF A LINKED BINARY TREE CLASS #####
########################################################
## AJ Zerouali, 2023/09/20
## Updated: 2023/09/20
## A binary tree implementation based on Ch.8 of
## "Data Structures and Algorithms in Python",
## by Goodrich, Tamassia, and Goldwasser.
## See also: https://github.com/mjwestcott/Goodrich

from collections import deque


class BinaryTree(object):
    
    TRAVERSAL_KEYWORDS = ["preorder", "postorder", "breadth_first", "inorder"]
    
    '''
        Linked binary tree class
    '''
    ###################################
    ### PRIVATE INTERNAL NODE CLASS ###
    ###################################
    class _Node(object):
        '''
            Private node class.
            This implementation doesn't account for
            the tree 
        '''
        # Pre-allocate 
        __slots__ = "_element", "_parent", "_left", "_right"
        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._num_children = 0
            self._update_num_children()
            
        def _update_num_children(self):
            self._num_children = int(self._left!=None)+int(self._right!=None)
        
            
    
    ###############################
    ### INTERNAL POSITION CLASS ###
    ###############################
    class Position(object):
        '''
            Position class for elements
            stored in a BinaryTree object.
            (See positional list)
            This class has 2 attributes:
            - The container, which is the binary tree.
            - The node, which is the object indexed by
              a Position.
        '''
        def __init__(self, container, node):
            '''
                Constructor. Invoqued only by BinaryTree class.
            '''
            # Container to which the position refers to
            # (here the container is the binary tree)
            self._container = container
            # Pointer to binary tree node
            self._node = node
            
            
        def element(self):
            '''
                Return element stored at current 
                position object.
            '''
            return self._node._element
        
        def __eq__(self, other):
            '''
                Return True if input "other" is a 
                Position representing same location
                as current position.
                (overloading of the "==" operator)
            '''
            return (type(other) == type(self)) and (other._node is self._node)
        
        def __ne__(self, other):
            '''
                Overloading of the "!=" operator
            '''
            return not (self == other)
    
    ### POSITION CREATION AND VALIDATION FUNCTIONS ### 
    def _validate(self, p):
        '''
            Return associated node if position p is valid
        '''
        if not isinstance(p, self.Position):
            raise TypeError("p must be a BinaryTree.Position object")
        if p._container is not self:
            raise ValueError("p does not belong to this BinaryTree object")
        # Convention for deprecated nodes
        if p._node._parent is p._node:
            raise ValueError("p is no longer a valid position")
        return p._node
    
    def _make_position(self, node):
        '''
            Return Position instance for a given node,
            or None if node is None
        '''
        if node != None:
            return self.Position(self, node)
        else:
            return None
            
    ################################
    ### LINKED BINARY TREE CLASS ###
    ################################
    def __init__(self):
        '''
            Constructor of linked binary tree class
        '''
        self._root = None
        self._size = 0
        
    ##### Node addition, deletion, and modification methods
    def _add_root(self, e):
        '''
            Add a root to current tree containing
            element e and return the root's Position.
            If tree already has a root, raises
            a ValueError.
        '''
        if self._root != None:
            raise ValueError("Root exists")
        self._root = self._Node(element = e)
        self._num_nodes = 1
        return self._make_position(self._root)
    
    def _add_left(self, p, e):
        '''
            Create left child for p
            storing element e, and return
            position of left child.
            Raises an error if p has
            a left child already.
        '''
        node = self._validate(p)
        # Case where p already has a left child
        if node._left != None:
            raise ValueError("Left child of p already exists")
        # Create left node
        node._left = self._Node(element = e, parent = node)
        
        # Update num children of node and num nodes in tree
        node._update_num_children()
        self._num_nodes += 1
        
        # Output
        return self._make_position(node._left)
    
    def _add_right(self, p, e):
        '''
            Create right child for p
            storing element e, and return
            position of right child.
            Raises an error if p has
            a right child already.
        '''
        node = self._validate(p)
        # Case where p already has a left child
        if node._right != None:
            raise ValueError("Left child of p already exists")
        # Create left node
        node._right = self._Node(element = e, parent = node)
        
        # Update number of children of node and num. nodes in tree
        node._update_num_children()
        self._num_nodes += 1
        
        # output
        return self._make_position(node._right)
    
    def _attach(self, p, T1, T2):
        '''
            Attach trees T1 and T2 to left and
            right as subtrees respectively of 
            node at position p.
            Raises an error if p is not a leaf.
            Raises an error if self, T1, and T2
            are not of the same class.
        '''
        # Check for errors
        if not self.is_leaf(p):
            raise ValueError("Cannot attach T1 and T2 as subtrees since node at p is not a leaf")
        if (type(self)!=type(T1)) or (type(self)!=type(T2)):
            raise TypeError("Current tree must be of same type as both T1 and T2")
        node = self._validate(p)
        
        # Attach T1 as left subtree of node
        if not T1.is_empty():
            T1._root._parent = node
            node._left = T1._root
            T1._root = None
            self._num_nodes += T1._num_nodes
            T1._num_nodes = 0
            
        # Attach T2 as right subtree of node
        if not T2.is_empty():
            T2._root._parent = node
            node._right = T2._root
            T2._root = None
            self._num_nodes += T2._num_nodes
            T2._num_nodes = 0
        
        # Update num children of node
        node._update_num_children()
        
    def _replace(self, p, e):
        '''
            Replace element stored at p by
            e, and return previously stored 
            element at p.
        '''
        node = self._validate(p)
        e_old = node._element
        node._element = e
        return e_old
    
    def delete(self, p):
        '''
            Delete node at position p, and:
            - If node at p has only one child, replace p 
              by this child node, and return element
              previously stored at position p.
            - If node at p has two children, raise an error.
            - If node at p has no children, return previously
              stored element.
        '''
        # Unwrap node at p (get parent and child)
        node = self._validate(p)
        if node._num_children == 2:
            raise ValueError("Cannot delete p as it has 2 children")
        element = node._element
        parent = node._parent # Could be the root
        if node._left != None:
            child = node._left
        elif node._right != None:
            child = node._right
        else:
            child = None
        
        # Modify child
        if child != None:
            child._parent = parent
        
        # Modify parent
        if parent == None:
            # If no parent then child is the new root
            self._root = child
        else:
            if node == parent._left:
                parent._left = child
            else:
                parent._right = child
        
        # Update num_nodes of tree
        self._num_nodes -= 1
        
        # Deprecate current node
        node._parent = node
                
        return element
    
    ##### Root, parent, and children methods
    def root(self):
        '''
            Return the position of the
            root of current tree.
        '''
        return self._make_position(self._root)
    
    def parent(self, p):
        '''
            Return position p's parent position
        '''
        node = self._validate(p)
        return self._make_position(node._parent)
    
    def sibling(self, p):
        '''
            Return a position corresponding to
            p's sibling if it exists and None 
            otherwise
        '''
        parent = self.parent(p)
        
        # Case where p is the root
        if parent == None:
            return None
        # Case where p is not the root
        else:
            if p==self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)
    
    def left(self, p):
        '''
            Return the left child of the node 
            at position p
        '''
        node = self._validate(p)
        return self._make_position(node._left)
        
    def right(self, p):
        '''
            Return the left child of the node 
            at position p
        '''
        node = self._validate(p)
        return self._make_position(node._left)
    
    def children(self, p):
        '''
            Get generator for children of node at
            position p.
        '''
        if self.left(p) != None:
            yield self.left(p)
        if self.right(p) != None:
            yield self.right(p)
    
    ##### Tree size and num. of children methods
    def __len__(self):
        '''
            Return number of positions/nodes in 
            current tree
        '''
        return self._num_nodes
    
    def num_children(self, p):
        '''
            Return num. of children of p
        '''
        node = self._validate(p)
        return node._num_children
    
    ##### Boolean verification methods
    def is_leaf(self, p):
        '''
            Return True if p is a leaf
        '''
        node = self._validate(p)
        return (node._num_children==0)
    
    def is_root(self, p):
        '''
            Return True if p is the root
            of current tree.
            p is the root if and only if
            its parent is None.
        '''
        return (self.root() == p)
    
    def is_empty(self):
        '''
            Return True if current tree is empty
        '''
        return (len(self)==0)
    
    ##### Depth and height methods
    def get_depth(self, p):
        if self.is_root(p):
            return 0
        else:
            return 1+self.get_depth(self.parent(p))
        
    def get_height(self, p):
        if self.is_leaf(p):
            return 0
        else:
            return 1+max(self.get_height(c) for c in self.children(p))
    
    ##### Traversal algorithms wrappers
    def preorder(self):
        '''
            Preorder traversal of tree,
            starting from the root.
        '''
        if not self.is_empty():
            for p in preorder(self, self.root()):
                yield p
    
    def postorder(self):
        '''
            Postorder traversal of tree,
            starting from the root.
        '''
        if not self.is_empty():
            for p in postorder(self, self.root()):
                yield p
    
    def inorder(self):
        '''
            Inorder traversal of tree,
            starting from the root.
        '''
        if not self.is_empty():
            for p in inorder(self, self.root()):
                yield p
    
    def breadth_first(self):
        '''
            Breadth first traversal
        '''
        if not self.is_empty():
            for p in breadth_first(self):
                yield p
    
    
    ##### Iterator generation methods
    def positions(self, traversal = "preorder"):
        '''
            Generate an iteration of all positions
            in the current tree, depending on the
            traversal algorithm selected.
        '''
        if traversal not in TRAVERSAL_KEYWORDS:
            raise ValueError("Unrecognized traversal algorithm")
        
        elif traversal == "preorder":
            return self.preorder()
        
        elif traversal == "postorder":
            return self.postorder()
        
        elif traversal == "inorder":
            return self.inorder()
        
        elif traversal == "breadth_first":
            return self.breadth_first()
    
    def __iter__(self):
        '''
            Generate an iteration of all elements
            stored in current tree            
        '''
        for p in self.positions():
            yield p.element()
            
            
'''
    TREE TRAVERSAL FUNCTIONS
'''
def preorder(T: BinaryTree, p: BinaryTree.Position):
    '''
        Preorder traversal of the subtree of 
        T rooted at position p.
        Yields an iterator for the subtree 
        positions.
    '''
    yield p
    
    for c in T.children(p):
        for other in preorder(T,c):
            yield other

def postorder(T: BinaryTree, p: BinaryTree.Position):
    '''
        Postorder traversal of the subtree of 
        T rooted at position p.
        Yields an iterator for the subtree 
        positions.
    '''
    
    for c in T.children(p):
        for other in preorder(T,c):
            yield other
    
    yield p
    
def inorder(T: BinaryTree, p: BinaryTree.Position):
    '''
        Inorder traversal of the subtree of 
        T rooted at position p.
        Yields an iterator for the subtree 
        positions.
    '''
    if T.left(p) != None:
        for other in inorder(T, T.left(p)):
            yield other
    
    yield p
    
    if T.right(p) != None:
        for other in inorder(T, T.right(p)):
            yield other
    
    
    def breadth_first(T: BinaryTree):
    '''
        Breadth first traversal of 
    '''
    if not T.is_empty():
        # Known positions not yet yielded
        pos_queue = deque()
        pos_queue.append(T.root())
        
        while len(pos_queue)>0:
            p = pos_queue.pop()
            yield p
            for c in T.children(p):
                pos_queue.append(c)