
class Dictionary:

    def __init__(self, labels):
        self.labels = labels

    def getIndex(self, label):
        return self.labels.index(label)

    def getLabel(self, index):
        return self.labels[index]
