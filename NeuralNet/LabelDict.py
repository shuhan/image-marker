
class Dictionary:

    def __init__(self, labels):
        self.labels = labels

    def getIndex(self, label):
        return self.labels.index(label)

    def count(self):
        return len(self.labels)

    def classes(self):
        return range(0, self.count())

    def getLabel(self, index):
        return self.labels[index]
