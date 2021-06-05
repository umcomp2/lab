class List_Head():
    def __init__(self):
        self.next = None
        self.prev = None

class List():
    def __init__(self):
        self.head = List_Head()
        self.head.next = self.head
        self.head.prev = self.head

    def empty(self):
        return self.head == self.head.next

    def _add(self, new, prev, next):
        new.next = next
        next.prev = new
        new.prev = prev
        prev.next = new

    def add(self, new):
        self._add(new, self.head, self.head.next)

    def add_tail(self, new):
        self._add(new, self.head.prev, self.head)

    def _delete(self, prev, next):
        prev.next = next
        next.prev = prev

    def delete(self, rm):
        self._delete(rm.prev, rm.next)

    def del_tail(self):
        list_delete(self.head.prev)

    def enqueue(self, new):
        self.add_tail(new)

    def dequeue(self):
        dq = None
        if not self.empty():
            dq = self.head.next
            self.delete(self.head.next)
        return dq

class Mem_Node(List_Head):
    # necesita exclusion mutua externa antes de modificar ref
    # mmap y mmunmap externos
    def __init__(self, mm, ref):
        self.mm = mm
        self.ref = ref
        super().__init__()

class Mem_List(List):
    def dequeue_ref(self, mmnode):
        dq = None
        if mmnode.next != self.head:
            dq = mmnode.next
        if mmnode != self.head and dq:
            mmnode.ref -= 1
            if mmnode.ref == 0:
                self.delete(mmnode)
        return dq
