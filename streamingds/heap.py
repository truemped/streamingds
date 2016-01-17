# vim: set fileencoding=utf-8 :
"""A collection of heap implementations with different storage backends.

The most simple one uses Pythons built in `heapq` in-memory module that can be
serialized using pickle.
"""
import heapq


class Heap(list):
    """A simple heap base class that defines a heap interface used by
    specialized implementations."""

    def min(self):
        """Return the heap's min element."""
        return self[0]

    def push(self, entry):
        heapq.heappush(self, entry)

    def pushpop(self, entry):
        return heapq.heappushpop(self, entry)

    def remove(self, entry):
        """This is O(2n) as list.remove is O(n) and heapq.heapify() as well."""
        if entry in self:
            super(Heap, self).remove(entry)
            heapq.heapify(self)
