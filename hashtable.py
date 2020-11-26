def _c_mul(value_a, value_b):
    '''Substitute for c multiply function'''
    return ((int(value_a) * int(value_b)) & 0xFFFFFFFF)

def nice_hash(input_string):
    '''Takes a string name and returns a hash for the string. This hash value
    will be os independent, unlike the default Python hash function.'''
    if input_string is None:
        return 0  # empty
    value = ord(input_string[0]) << 7
    for char in input_string:
        value = _c_mul(1000003, value) ^ ord(char)
    value = value ^ len(input_string)
    if value == -1:
        value = -2
    return value

class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next_node = None

    def __repr__(self):
        """ Returns the str repr of the node and all subsequent nodes """
        this_node = f'{self.key}:{self.value} -> '
        following_nodes = repr(self.next_node)
        return this_node + following_nodes

    def __len__(self):
        """ Returns the length of the list starting from self """
        if self.next_node:
            return 1 + len(self.next_node)
        else:
            return 1

class HashTable:
    """A chaining hash table to store (key, value) pairs.
       You should use the default hash function for key objects as
       the basis for determining which slot items go/are in,
       eg, hash(key)
       In the assignment context the keys will be Names and values
       will be (nhi, result) tuples.
       You should be able to add other objects when testing,
       as long as they are hashable with hash(my_testing_thing)...
       But make sure you test it with Name objects as this will let
       you compare your comparisons_used with the actual comparisons used.
       ************************************************************************
       ************************************************************************
       *** DON'T add/remove/change any methods except the get_value method! ***
       ************************************************************************
       ************************************************************************
    """
    # class variables - used for keeping track of number of pointers used.
    # each slot uses one pointer to point ot the head of the linked list
    # in that slot and each node uses one pointer to point to the next node
    # This variable doesn't include memory used for the data in each node.
    _memory_used = 0

    def __init__(self, initial_size):
        """ Initialises a hash table with initial_size slots.
            The slots are basically stored as a linked list of Nodes.
            The performance counters are all set to zero.
        """
        self.comparisons_used = 0
        self.number_of_slots = initial_size
        self._number_of_items = 0

        # setup the given number of slots, each containing None
        # Note: self._data[i] will be the head of a linked list
        self._data = [None] * initial_size
        HashTable._memory_used += initial_size
        #StatCounter.increment(HASH_TABLES_CREATED)

    def store_pair(self, key, value):
        """
        Stores the key, value pair in the hash table.
        Uses the hash of the key to get the index to store the pair.
        You should make a new node using the given key and value and insert it
        at the start of the linked list in the indexed slot in self._data
        """
        slot_index = nice_hash(key) % self.number_of_slots
        head = self._data[slot_index]
        new_node = Node(key, value)
        if head is None:
            self._data[slot_index] = new_node
        else:
            new_node.next_node = head
            self._data[slot_index] = new_node
        self._number_of_items += 1
        HashTable._memory_used += 1

    def get_value(self, key):
        """ Returns the first value associated with the key.
            If the key isn't in the table then None is returned.
        """
        # ---start student section---
        values = []
        slot_index = nice_hash(key) % self.number_of_slots
        head = self._data[slot_index]
        while not head is None:
            self.comparisons_used += 1
            if head.key == key:
                values.append(head.value)            
            head = head.next_node
        if len(values) > 0:
            return values
        else:
            return ['Other']
            
        # ===end student section===

    def __repr__(self):
        """ This is rather ugly, you are better to do a print(my_hashtable)
        which will use the __str__ method to give more readable output.
        """
        return repr(self._data)

    def __str__(self):
        string_thing = 'HashTable:\n'
        for slot_index, head_node in enumerate(self._data):
            string_thing += f'{slot_index:6}: {repr(head_node)}\n'
        string_thing += (f'Num of items = {self._number_of_items}\n')
        string_thing += (f'Num of slots = {self.number_of_slots}\n')
        string_thing += (f'Load factor  = {self.load_factor():.2f}')
        return string_thing

    #def __eq__(self, other):
        #return self._data == other._data

    def __len__(self):
        return len(self._data)

    def __contains__(self, item):
        """ You aren't completing this method.
            You need to complete the contains method
            You could use the following instead (but you shouldn't need to):
                your_table.get_value(key_to_find) is not None
        """
        raise TypeError(
            "You can't use the 'in' keyword with a HashTable")

    def load_factor(self):
        """ Returns the load factor for the hash table """
        return self._number_of_items / self.number_of_slots

    def index(self, start=None):
        """ Points out that we can't do this! """
        raise TypeError(f"{type(self)} doesn't allow using index")

    def __getitem__(self, i):
        """ You can't directly index into HashTables, eg,
        ht = Hashtable(11)
        item0 = ht[0]  # won't work
        You should use your_table.get_value(key_to_find) instead.
        """
        raise IndexError(f"You can't directly index into Hashtables")

    @classmethod
    def get_memory_used(cls):
        """ Returns the amount of memory used """
        return cls._memory_used

    @classmethod
    def reset_memory_used(cls):
        """ Resets the the memory tracker """
        cls._memory_used = 0

# ----------------- End of HashTable class ----------------------------