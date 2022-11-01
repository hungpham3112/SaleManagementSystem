class Node:
    def __init__(self, data):
        self.data = data
        self.next: Node | None = None
        self.prev: Node | None = None

    def __getitem__(self):
        return self.data

    def set_current(self, new_data):
        self.data = new_data

    def get_next(self):
        return self.next

    def set_next(self, next_data):
        self.next = next_data
