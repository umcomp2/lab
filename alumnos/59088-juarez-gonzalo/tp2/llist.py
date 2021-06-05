class List_Head():
    def __init__(self):
        self.next = None

class List():
    def __init__(self):
        self.head = List_Head()
        self.tail = self.head

    def empty(self):
        return self.head == self.tail

    def print_list(self):
        print("======start")
        curr = self.head
        while curr:
            print(curr, curr.__dict__)
            curr = curr.next
        print("======iend")

    def add(self, new):
        self.tail.next = new
        self.tail = new

    def delete(self, rm):
        curr = self.head
        while curr.next != rm:
            curr = curr.next
        curr.next = rm.next
        if rm == self.tail:
            self.tail = curr

class Mem_Node(List_Head):
    # necesita exclusion mutua externa antes de modificar ref
    # mmap y mmunmap externos
    def __init__(self, mm, ref):
        self.mm = mm
        self.ref = ref
        super().__init__()
