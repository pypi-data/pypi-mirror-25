from epiphany.support.collection import Collection


class Queue(Collection):
    def __init__(self, collection):
        super().__init__(collection)
        self.collection = super().queue()


    def __iter__(self):
        return iter(self.collection)


    def __next__(self):
        return self.collection.popleft()


    def __contains__(self, item):
        return item in self.collection


    def valid(self) -> bool:
        return True if len(self.collection) is not 0 else False

