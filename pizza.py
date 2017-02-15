
class Pizza(object):

    sizeX = 0
    sizeY = 0
    sliceSize = 0
    countIng = 0
    pizza = None
    alloc = None
    window = None

    def __init__(self, filename):
        file = open(filename, "r")
        self._initParams(file.readline())
        self._initPizza(file)
        self._initWindow()

        print(self.window)


    def _initParams(self, line):
        line = line.replace("\n", "")
        line = line.split(" ")
        self.sizeX = int(line[0])
        self.sizeY = int(line[1])
        self.countIng = int(line[2])
        self.sliceSize = int(line[3])
        self.pizza = [[0 for x in range(self.sizeY)] for y in range(self.sizeX)]
        self.alloc = [[0 for x in range(self.sizeY)] for y in range(self.sizeX)]

    def _initPizza(self, file):
        row = 0
        for line in file:
            line = line.replace("\n"," ").replace("T", "0 ").replace("M", "1 ").strip(" ").split(" ")
            col = 0
            for ing in line:
                self.pizza[row][col] = int(ing)
                col += 1

            row += 1

    def _initWindow(self):
        self.window = [[self._getPoint(x,y) for x in range(2)] for y in range(self.countIng*2)]


    def _getPoint(self, x, y):
        if x == 0:
            return y%self.countIng
        if x == 1:
            return y//self.countIng

def main():
    p = Pizza("small.in")

if __name__ == '__main__':
    main()
