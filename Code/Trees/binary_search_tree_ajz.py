from .linked_binary_tree import LinkedBinaryTree
from collections.abc import MutableMapping

# From: https://github.com/mjwestcott/Goodrich/blob/master/ch10/map_base.py
class MapBase(MutableMapping):
    """Our own abstract base class that includes a nonpublic _Item class."""
    #------------------------------- nested _Item class -------------------------------
    class _Item:
        """Lightweight composite to store key-value pairs as map items."""
        __slots__ = '_key', '_value'
        
        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key   # compare items based on their keys

        def __ne__(self, other):
            return not (self == other)       # opposite of __eq__

        def __lt__(self, other):
            return self._key < other._key    # compare items based on their keys

        
# Based on: https://github.com/mjwestcott/Goodrich/blob/master/ch11/binary_search_tree.py
class BSTMap(LinkedBinaryTree, MapBase):
    '''
        Implementation of a map as a
        binary search tree.
        No rebalancing done in this version.
    '''
    #---------- Nested Position class ----------
    class Position(LinkedBinaryTree.Position):
        '''
            Abstract position class for nodes
            of BST
        '''
        def key(self):
            '''
                Return key attribute of item contained in current position
            '''
            return self.element()._key
        
        def value(self):
            '''
                Return value attribute of item contained in current position
            '''
            return self.element()._value
    
    #---------- Private tree search methods ----------
    def _search_subtree(self, p, k):
        '''
            Search for key k in subtree
            rooted at position p.
            Assumes tree is non-empty.
        '''
        if k<p.key() and self.left(p) is not None:
            return self._search_subtree(self.left(p), k)
        elif k==p.key():
            return p
        elif k>p.key() and self.right(p) is not None:
            return self._search_subtree(self.right(p), k)
        return p
    
    def _subtree_first_position(self, p):
        '''
            Return position of first item
            in subtree rooted at p.
        '''
        cur_pos = p
        while self.left(cur_pos) is not None:
            cur_pos = self.left(cur_pos)
        return cur_pos
    
    def _subtree_last_position(self, p):
        '''
            Return position of last item
            in subtree rooted at p.
        '''
        cur_pos = p
        while self.right(cur_pos) is not None:
            cur_pos = self.right(cur_pos)
        return cur_pos
            
    #---------- Private tree restructuring methods ----------
    '''
        To be implemented in subclasses of BSTMap()
    '''
    def _rebalance_insert(self, p):
        pass
    def _rebalance_delete(self, p):
        pass
    def _rebalance_access(self, p):
        pass
    
    def _relink(self, p):
        pass
    
    def _rotate(self, p):
        pass
    
    def _trinode_restructure(self, p):
        pass
    #---------- Public Map methods ----------
    def __getitem__(self, k):
        '''
            Search for key k in map and
            return associated value.
            Implements the call M[k]
        '''
        if self.is_empty():
            raise ValueError("Map is empty")
        p = self._search_subtree(self.root(), k)
        if k==p.key():
            return p.value()
        else:
            raise ValueError(f"Key \'{repr(k)}\' not found")
    
    def __iter__(self):
        '''
            Generate iterator over all keys in increasing order.
        '''
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)
    
    def __setitem__(self, k, v):
        '''
            Assign value v to key k.
        '''
        # If tree is empty, add (k,v) as root
        if self.is_empty():
            root = self._add_root(self._Item(k,v))
            self._rebalance_insert(root)
        # If tree is not empty, search for key
        else:
            p = self._search_subtree(self.root(), k)
            
            # If k already exists in tree, replace value
            if k == p.key():
                p.element()._value = v
                self._rebalance_access(p)
                return
            # If k doesn't exist, add node containing (k,v)
            else:
                if k<p.key():
                    node = self._add_left(p, self._Item(k,v))
                elif k>p.key():
                    node = self._add_right(p, self._Item(k,v))
                
                # Rebalance at node
                self._rebalance_insert(node)
    
    def delete(self, p):
        '''
            Delete item at position p and
            reshape tree to preserve BST
            property. Calls:
            - LinkedBinaryTree._delete(Position).
            - LinkedBinaryTree._replace(Position1, Position2).
        '''
        self._validate(p)
        
        # Case where p has two children
        if (self.left(p) is not None) and (self.right(p) is not None):
            replacement_pos = self._subtree_last_position(self.left(p))
            self._replace(p, replacement_pos)
            p = replacement_pos
        
        # Case where p (now) has at most one child
        parent = self.parent(p)
        self._delete(p)
        self._rebalance_delete(parent)
    
    def __delitem__(self, k):
        '''
            Delete item with key k from
            map. Calls delete(Position)
            method.
        '''
        if self.is_empty():
            raise ValueError("Map is empty.")
        else:
            # BST search for node containing key k
            p = self._search_subtree(self.root(), k)
            if k == p.key():
                # Call delete position method
                self.delete(p)
                return
            else:
                self._rebalance_access(p)
                raise ValueError(f"Key \'{repr(k)}\' not found")
    
    #---------- Public tree navigation methods ----------
    
    def first(self):
        '''
            Return first Position in tree
            (i.e. position of lowest key)
        '''
        # Empty tree case
        if len(self) == 0:
            return None
        else:
            return self._subtree_first_position(self.root())
    
    def last(self):
        '''
            Return last Position in tree
            (i.e. position of greatest key)
        '''
        # Empty tree case
        if len(self) == 0:
            return None
        else:
            return self._subtree_last_position(self.root())
    
    def before(self, p):
        '''
            Return Position just before p
            in BST order.
        '''
        self._validate(p)
        # If p has a left child, search for last position
        if self.left(p) is not None:
            return self._subtree_last_position(self.left(p))
        # If p does not have a left child, walk upward
        ## in tree until ancestor is a right child
        ## If p.key() is lowest, returns None.
        else:
            cur_pos = p
            cur_pos_parent = self.parent(cur_pos)
            while (cur_pos_parent is not None) and (cur_pos==self.left(cur_pos_parent)):
                cur_pos = cur_pos_parent
                cur_pos_parent = self.parent(cur_pos)
            return cur_pos_parent
    
    def after(self, p):
        '''
            Return Position right after p
            in BST order.
        '''
        self._validate(p)
        # If p has a left child, search for last position
        if self.right(p) is not None:
            return self._subtree_first_position(self.right(p))
        # If p does not have a left child, walk upward
        ## in tree until ancestor is a right child
        ## If p.key() is lowest, returns None.
        else:
            cur_pos = p
            cur_pos_parent = self.parent(cur_pos)
            while (cur_pos_parent is not None) and (cur_pos==self.right(cur_pos_parent)):
                cur_pos = cur_pos_parent
                cur_pos_parent = self.parent(cur_pos)
            return cur_pos_parent