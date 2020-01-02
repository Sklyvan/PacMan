class Node:
    def __init__(self, NodeData):
        self.Data = NodeData
        self.Next = None
        self.Prev = None

    def GetDataType(self):
        return type(self.Data)

    def __str__(self):
        return str(self.Data)


class Circular_LinkedList:
    def __init__(self):
        self.Initial = None
        self.Size = 0

    def isEmpty(self):
        if self.Size == 0:
            return True
        return False

    def Add(self, NodeData):
        MyNode = Node(NodeData)
        if self.isEmpty():
            self.Initial = MyNode
            MyNode.Next = MyNode
            MyNode.Prev = MyNode
            self.Size += 1
            return MyNode
        else:
            Current = self.Initial
            Aux = Current.Prev
            Aux.Next = MyNode
            MyNode.Next = Current
            Current.Prev = MyNode
            MyNode.Prev = Aux
            self.Size += 1
            return MyNode

    def Remove(self, NodeData):
        SearchLoop = True
        Current = self.Initial
        while SearchLoop:
            if Current.Data == NodeData:
                AuxNext = Current.Next
                AuxPrev = Current.Prev
                AuxPrev.Next = AuxNext
                AuxNext.Prev = AuxPrev
                if Current == self.Initial:
                    self.Initial == AuxNext
                SearchLoop = False
                self.Size -= 1
                return True

            else:
                Current = Current.Next
                if Current == self.Initial:
                    SearchLoop = False
                    return False

    def __len__(self):
        return self.Size

    def __str__(self):
        String = "["
        Size = len(self)
        Current = self.Initial
        for i in range(Size):
            Str = Current.Data
            String += str(Str)
            if i != Size - 1:
                String += str(", ")
            Current = Current.Next
        String += str("]")

        return String
