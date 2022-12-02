"""A circular genome for simulating transposable elements."""

from __future__ import annotations
from typing import (
    Generic, Iterable, TypeVar, Protocol
)

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)

from typing import (
    Generic, TypeVar, Protocol)

class Comparable(Protocol):
    """Type info for specifying that objects can be compared with <."""

    def __lt__(self, other: Comparable) -> bool:
        """Less than, <, operator."""
        ...


T = TypeVar('T')
S = TypeVar('S', bound=Comparable)


class Link(Generic[T]):
    """Doubly linked link."""

    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create a new link and link up prev and next."""
        self.val = val
        self.prev = p
        self.next = n


def insert_after(link: Link[T], val: T) -> None:
    """Add a new link containing val after link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link


#Example from Thomas Abstract Genome Class 

class Genome(ABC):
    """Representation of a circular genome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet
        
    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet



class ListGenome(Genome):
    """
    Representation of a genome.
    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = ['-']*n # portion of genome that is not inactive or active TE is represented as "-"
                                #accoring to line 124 in example abstract genome class 
        self.te = dict() # self.te is a dictonary so we can store TE id as key, and map position and length to that id 
        self.id = 0 # the first id will be 0 

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.
        Insert a new transposable element at position pos and len
        nucleotide forward.
        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.
        Returns a new ID for the transposable element.
        """
        self.id += 1 #reminder that self.id is the index number of transcriptional element, starts at 0 so first will be 1
        self.te[self.id] = [pos, length] # new item in self.te dictionary at with the index [self.id]
                                         # in index of self.if, [0] = pos, [1]= length (supplied in input of class)
        key_list = list(self.te.keys()) # keys() is a built in python method (idea from Sara) that calls all the keys of a dictionary 
        for key in key_list: # this for loop: 
            #1. establishes where new te should go 
            #2. checks to see if there is already a te there and converts it to inactive if so
            #3. inserts the new te into the genome 
            start = self.te[key][0] #see line 156
            end = start + self.te[key][1] #see line 156

            if start < pos <= end: # check to see if there is already a te in location where new te wants to go 
                                   # this works because we havent reassined pos to the index of the new te yet. 
                for i in range(start, end): # this loop changes preexisting te to inactive 
                    self.genome[i] = 'x' 
                del self.te[key] #we need to delete the key of the inactivated te from dictionary since there is a new te in that index on genome 

            if pos < start: #this statement moves the 'x' features of old te to their new loccation 
                new_start = start + length 
                self.te[key][0] = new_start #because we deleted this value in line 169, need to update where old te is in dictionary  
        transcriptional_element = ['A'] * length # assign new TE per assignment 
        self.genome[pos:pos] = transcriptional_element #put in the new te we created in line above in correct place 
                                                        #(reminder pos is one of the inputs for class)
        return self.id #index number of new transcriptional element in genome 

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.
        Copy the transposable element te to an offset from its current
        location.
        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.
        If te is not active, return None (and do not copy it).
        """
        if te in self.te.keys(): # if input is in the dictionary (need to go through keys list to limit computational time) 
            position = (self.te[te][0] + offset) % len(self) # from Sara and Laura, see line 156 but tbh im not sure how this works
                                                      # position needs to be in terms of % len 
            length = self.te[te][1] # see line 156
            self.insert_te(position, length) #pos = p, length= l 
            return self.id
        else:
            return None

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.
        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        if te in self.te.keys(): #we are given te as an integer, it is the index number of the te,
                                 #which is the key in our dictionary that maps to the position [0] and length [1]
            start = self.te[te][0] 
            end = start + self.te[te][1] 
            for i in range(start, end): 
                self.genome[i] = 'x' #x marks that it is inactivated 
            del self.te[te]
        return None
            
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.te.keys())  

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome) 

    def __str__(self) -> str:
        """
        Return a string representation of the genome.
        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.
        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return ''.join(self.genome) # easy to join lists into a string 


#Initial class copied from https://github.com/birc-ctib-2022/doubly-linked-lists-tessdiv 
#and from https://github.com/birc-ctib-2022/doubly-linked-lists-tessdiv/blob/main/src/lists.py

class DLList(Generic[T]):
    """
    Wrapper around a doubly-linked list.
    This is a circular doubly-linked list where we have a
    dummy link that function as both the beginning and end
    of the list. By having it, we remove multiple special
    cases when we manipulate the list.
    >>> x = DLList([1, 2, 3, 4])
    >>> print(x)
    [1, 2, 3, 4]
    """

    head: Link[T]  # Dummy head link

    def __init__(self, seq: Iterable[T] = ()):
        """Create a new circular list from a sequence."""
        # Configure the head link.
        # We are violating the type invariants this one place,
        # but only here, so we ask the checker to just ignore it.
        # Once the head element is configured we promise not to do
        # it again.
        self.head = Link(None, None, None)  # type: ignore
        self.head.prev = self.head
        self.head.next = self.head

        # Add elements to the list, exploiting that self.head.prev
        # is the last element in the list, so appending means inserting
        # after that link.
        for val in seq:
            insert_after(self.head.prev, val)

    def __str__(self) -> str:
        """Get string with the elements going in the next direction."""
        elms: list[str] = []
        link = self.head.next
        while link and link is not self.head:
            elms.append(str(link.val))
            link = link.next
        return f"[{', '.join(elms)}]"
    __repr__ = __str__  # because why not?

class LinkedListGenome(Genome):
    """
    Representation of a genome.
    Implements the Genome interface using linked lists.
    """
#COMMENTS ARE WHERE IMPLEMENTATION IS DIFFERENT FROM LISTS 
    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = DLList(['-']*n) # use DLList __init__ from exercises 
        self.te = dict() 
        self.id = 0 

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.
        Insert a new transposable element at position pos and len
        nucleotide forward.
        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.
        Returns a new ID for the transposable element.
        """
        self.id += 1 
        self.te[self.id] = [pos, length] 
        key_list = list(self.te.keys()) 
        for key in key_list: 
            start = self.te[key][0] 
            end = start + self.te[key][1] 
            if start < pos <= end: 
                self.disable_te(key)
            if pos < start:
                new_start = start + length 
                self.te[key][0] = new_start 
        te = DLList(['A'] * length) #new te needs to be made of 'A' per assignment, note how its made with DLL class 
        link_start = self.genome.head #reminder .head is first element 
        i = 0 
        while i < start: 
            link_start = link_start.next 
            i += 1
        link_e = link_start.next 
        link_start.next = te.head.next
        te.head.next.prev = link_start
        link_e.prev = te.head.prev
        te.head.prev.next = link_e
        return self.id 

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.
        Copy the transposable element te to an offset from its current
        location.
        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.
        If te is not active, return None (and do not copy it).
        """
        if te in self.te.keys(): 
            start = self.te[te][0] 
            length = self.te[te][1] 
            offset = offset % len(self) 
            te_start = start + offset
            self.insert_te(te_start, length)
            return self.id
        return None
    
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.
        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
    
        if te in self.te.keys(): 
            start = self.te[te][0] 
            length = self.te[te][1] 
            disabled_te = DLList(['x']*length) #make a doubly-linked list for the te to be disabled 
            link_start = self.genome.head 
            i = 0 
            while i < start: 
                link_start = link_start.next 
                i += 1
            link_end = link_start 
            j = 0
            while j <= length:
                link_end = link_end.next 
                j += 1
            
            link_start.next = disabled_te.head.next
            disabled_te.head.prev.next = link_end
            link_end.prev = disabled_te.head.prev
            disabled_te.head.next.prev = link_start
            del self.te[te] 
        return None

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.te.keys())  

    def __len__(self) -> int:
        """Current length of the genome."""
        #more complicated because can only use len() method for simple list 
        length = 0 # new variable, begin with 0 
        link = self.genome.head.next #self.genome.head will be the same as self.genome.head.next when DLL is empty
        while link and link is not self.genome.head: 
            length += 1 # similar to initial lists exercise 
            link = link.next # link in this case functions kind of like an accumulator 
        return length 

    def __str__(self) -> str:
        """
        Return a string representation of the genome.
        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.
        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        elms: str = ''
        link = self.genome.head.next
        while link and link is not self.genome.head:
            elms += (str(link.val))
            link = link.next
        return elms 