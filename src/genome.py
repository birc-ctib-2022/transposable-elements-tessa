"""A circular genome for simulating transposable elements."""

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)


class Genome(ABC):
    """Representation of a circular enome."""

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
        ...  # FIXME
        self.genome = ['-']*n #from line 82, locations on genome with no TE should be '-'
        self.te = dict() #if i make the te a dictionary i can make the id as key with where they are and how long in dictionary
        self.id= 0 


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
        ...  # FIXME
        self.id += 1 #start with first id 
        self.te[self.id]= [pos,length] #take input defined when i established class, put it in self.te library
                                       #with id equal to +1 (from start equal to 0)
                                       #in self.te library key index 0= pos (input for class)
                                       #key index 1 is the length (also input for class)
        key_list = list(self.te.keys()) #make a new variable that is a list of they keys from self.te 
                                        # key() is a built in python method "The keys() method in 
                                        # Python Dictionary, 
                                        # returns a view object that displays a list of all 
                                        # the keys in the dictionary in order of insertion using Python."
        for key in key_list:            #iterate through list
            start = self.te[key][0]     #make a new variable that is what key[0] in self.te dictionary corresponds to see line 120  
            end = start + self.te[key][1]       #similar to above but end should be 1 see line 121
            if start < pos <= end:       # if the new te pos is in the range the previous te, the previous te must be inactivated 
                for i in range(start, end):
                    self.genome[i] = 'x' #make te inactive (see line 83)
            del self.te[key]
        if pos < start:
            new_start = start + length #new variable for new te
            self.te[key][0]= new_start
        te= ['A']*length  #see line 82
        self.genome[pos:pos] = te
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
        ...  # FIXME
        if te in self.te.keys():
            p= (self.te[te][0] + offset) % len(self)  # got help from Sara and Laura here 
            l= self.te[te][1]
            self.insert_te (p,l)
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
        ...  # FIXME
        if te in self.te.keys(): #if te exists 
            start = self.te[te][0] #te is the integer provided in this class that 
                                    #correponds to the te that needs to be disabled
                                   #index corresponds to key for dictionary self.te
            end = start + self.te[te][1]
            for i in range (start, end):
                self.genome [i] = 'x' #see line 83
            del self.te[te]  #delete so that 
                             #if statement cause infinite loop and so we dont 
                             # #mess with the dictionary construction 
        return None


    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # FIXME
        return list(self.te.keys()) #easy because its a list so can use keys method for ids


    def __len__(self) -> int:
        """Current length of the genome."""
        ...  # FIXME
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
        return ''.join(self.genome)



class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        ...  # FIXME

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
        ...  # FIXME
        return -1

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
        ...  # FIXME

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        # FIXME
        return []

    def __len__(self) -> int:
        """Current length of the genome."""
        # FIXME
        return 0

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
        return "FIXME"
