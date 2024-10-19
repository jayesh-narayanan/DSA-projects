class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item from the stack. Raise an error if the stack is empty."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.items.pop()

    def top(self):
        """Return the top item from the stack without removing it. Raise an error if the stack is empty."""
        if self.is_empty():
            raise IndexError("Top from empty stack")
        return self.items[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self.items)