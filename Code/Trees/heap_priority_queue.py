# From: https://github.com/mjwestcott/Goodrich/blob/master/ch09/priority_queue_base.py
class PriorityQueueBase:
    """Abstract base class for a priority queue."""

    #------------------------------ nested _Item class ------------------------------
    class _Item:
        """Lightweight composite to store priority queue items."""
        
        __slots__ = '_key', '_value'
        
        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key    # compare items based on their keys

        def __repr__(self):
            #return '({0},{1})'.format(self._key, self._value) #Original
            return f"({self._key}, {self._value})"

    #------------------------------ public behaviors ------------------------------
    def is_empty(self):                  # concrete method assuming abstract len
        """Return True if the priority queue is empty."""
        return len(self) == 0
    
    def __len__(self):
        """Return the number of items in the priority queue."""
        raise NotImplementedError('must be implemented by subclass')
    
    def add(self, key, value):
        """Add a key-value pair."""
        raise NotImplementedError('must be implemented by subclass')
        
    def min(self):
        """
            Return but do not remove (k,v) tuple with minimum key.
            Raise ValueError if empty.
        """
        raise NotImplementedError('must be implemented by subclass')
        
    def remove_min(self):
        """
            Remove and return (k,v) tuple with minimum key.
            Raise Empty exception if empty.
        """
        raise NotImplementedError('must be implemented by subclass')
        
# This is my version of: https://github.com/mjwestcott/Goodrich/blob/master/ch09/heap_priority_queue.py
class HeapPriorityQ(PriorityQueueBase):
    '''
        Implementation of a priotiy queue 
        as an array-based heap.
    '''
    #---------- Constructor ----------
    def __init__(self):
        '''
            Constructor for priority queue
        '''
        self._data = []
        
    #---------- Private methods ----------
    
    def _parent(self, i):
        '''
            Return index of parent of node at position i.
            (Should not be called for the root)
        '''
        return (i-1)//2
    
    def _left_child(self,i):
        '''
            Return index of left child of node at position i.
        '''
        return 2*i+1
    
    def _has_left(self, i):
        '''
            Check if node at index i has a left child.
        '''
        return self._left_child(i)<len(self._data)
    
    def _right_child(self,i):
        '''
            Return index of right child of node at position i.
        '''
        return 2*(i+1)
    
    def _has_right(self, i):
        '''
            Check if current index has a left child.
        '''
        return self._right_child(i)<len(self._data)
    
    def _swap(self, i, j):
        '''
            Interchange items in nodes at positions
            i and j.
        '''
        self._data[i], self._data[j] = self._data[j], self._data[i]
        
    def _bubble_up(self, i):
        '''
            Execute up-heap bubbling on node
            at position i.
        '''
        # Check that i is not the root
        if i>0:
            j = i
            p = self._parent(j)
            
            # Core loop
            while self._data[j]<self._data[p] and j>0:
                self._swap(j,p)
                j, p = p, self._parent(p)
    
    def _bubble_down(self, i):
        '''
            Execute down-heap bubbling on node
            at position i.
        '''
        # Check that node has a left child at least
        ## If False, then current index is in highest level of heap
        if self._has_left(i):
            lchild = self._left_child(i)
            min_child = lchild
            
            # Check if node has right child and if lower than left child
            if self._has_right(i):
                rchild = self._right_child(i)
                if self._data[rchild]<self._data[lchild]:
                    min_child = rchild
            
            # Check if i and min_child need swap
            if self._data[min_child]<self._data[i]:
                self._swap(min_child, i)
                self._bubble_down(min_child)
            
        
    
    #---------- Public methods ----------
    def __len__(self):
        '''
            Return number of elements stored in the priority queue
        '''
        return len(self._data)
    
    def min(self):
        '''
            Return (key, value) tuple corresonding to minimal element 
            of the priority queue.
            Raises ValueError if the queue is empty.
        '''
        if self.is_empty():
            raise ValueError("Cannot return min element of an empty priority queue")
        
        item = self._data[0]
        return (item._key, item._value)
    
    def add(self, k,v):
        '''
            Add key-value item (k,v) to the priority queue,
            in such a way that the complete binary tree
            and the heap-order properties are satisfied
        '''
        # Append new item to base array
        self._data.append(self._Item(k,v))
        
        # Execute up-heap bubbling
        self._bubble_up(len(self._data)-1)
        
    
    def remove_min(self):
        '''
            Remove and return minimal element of the priority
            queue, and reshape heap.
            Raises ValueError if tree is empty
        '''
        # Raise error if heap is empty
        if self.is_empty():
            raise ValueError("Cannot remove minimal element of an empty priority queue")
            
        # Swap root and last entry of heap
        self._swap(0, len(self._data)-1)
        min_element = self._data.pop()
        
        # Execute down-heap bubbling
        self._bubble_down(0)
        
        # Output
        return (min_element._key, min_element._value)