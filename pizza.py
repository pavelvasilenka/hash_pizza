#
#
#
class Pizza(object):

    sizeX = 0
    sizeY = 0
    sliceSize = 0
    countIng = 0
    pizza = None
    alloc = None
    windows = []

    def __init__(self, filename):
        file = open(filename, "r")
        self._initParams(file.readline())
        self._initPizza(file)
        self._initWindows()


    def allocateClusters(self):
        self.windows[0].getCluster()
        self.windows[0].moveRight()
        self.windows[0].getCluster()
        self.windows[0].moveRight()
        self.windows[0].getCluster()
        self.windows[0].moveRight()
        self.windows[0].getCluster()
        self.windows[0].moveRight()
        self.windows[0].getCluster()
        self.windows[0].moveRight()
        self.windows[0].getCluster()
        self.windows[0].moveRight()
        self.windows[0].getCluster()
        self.windows[0].moveRight()
        self.windows[0].getCluster()

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
            print(line)
            col = 0
            for ing in line:
                self.pizza[row][col] = int(ing)
                col += 1

            row += 1

    def _initWindows(self):
        cells = [[self._getPoint(x,y) for x in range(2)] for y in range(self.countIng*2)]
        self.windows.append(Window(cells, self.sizeX, self.sizeY, self.pizza, self.countIng))

    def _getPoint(self, x, y):
        if x == 0:
            return y%self.countIng
        if x == 1:
            return y//self.countIng

#
#
#
class Window(object):

    cells = None
    sizeX = 0
    sizeY = 0
    pizza = None
    countIng = 0

    def __init__(self, cells, sizeX, sizeY, pizza, countIng):
        self.cells = cells
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.pizza = pizza
        self.countIng = countIng

    def moveDown(self):
        if self._canMoveDown():
            for cell in self.cells:
                cell[0] += 1


    def moveRight(self):
        if self._canMoveRight():
            for cell in self.cells:
                cell[1] += 1

    #
    #
    #
    def _hasCluster(self):
        print(self.cells)
        sum = 0
        for cell in self.cells:
            sum += self.pizza[cell[0]][cell[1]]

        if sum >= self.countIng:
            return True

        return False

    #
    #
    #
    def getCluster(self):
        print(self._hasCluster())
        return Cluster(self.cells)

    #
    #
    #
    def _canMoveDown(self):
        if self.cells[len(self.cells) - 1][0] + 1 < self.sizeX:
            return True

        return False

    #
    #
    #
    def _canMoveRight(self):
        if self.cells[len(self.cells) - 1][1] + 1 < self.sizeY:
            return True

        return False


#
#
#
class Cluster(object):

    cells = None

    def __init__(self, cells):
        self.cells = cells

#
#
#
def main():
    p = Pizza("small.in")
    p.allocateClusters()

if __name__ == '__main__':
    main()
