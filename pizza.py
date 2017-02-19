import copy
import numpy as np

#
#
#
class Pizza(object):

    sizeX = 0
    sizeY = 0
    sliceSize = 0
    countIng = 0
    pizza = None
    alloc = []
    windows = []
    results = []
    clusters = []


    def __init__(self, filename):
        file = open(filename, "r")
        self._initParams(file.readline())
        self._initPizza(file)
        self._initWindows()

    def cut(self):
        i = 0
        self.clusters.append([])
        for window in self.windows:
            window.alloc = self.alloc
            window.clusterCount = len(self.clusters[i])

            cluster = window.getCluster(len(self.clusters[i])+1 )
            if cluster is not None:
                self.clusters[i].append(cluster)

            self._cut(window, i)
            self.alloc = window.alloc
            #i +=1

        print("\nInitial clusters:")
        for c in self.alloc:
            print(c)

        print("\nstart resizing...")
        for cluster in self.clusters[i]:
            self.alloc = cluster.resize(self.alloc, self.sliceSize)

        print("\nCut pizza:")
        for c in self.alloc:
            print(c)

        sum = 0
        for row in self.alloc:
            for el in row:
                if el != 0:
                    sum += 1

        self.results.append(sum)
        print("Covered ", sum, " cells out of ", self.sizeX*self.sizeY)

    def cut_1(self):
        i = 0
        for window in self.windows:
            self.clusters.append([])

            cluster = window.getCluster()
            if cluster is not None:
                self.clusters[i].append(cluster)

            self._cut(window, i)
            self.alloc = window.alloc

            print("\nInitial clusters:")
            for c in window.alloc:
                print(c)


            print("\nstart resizing...")
            for cluster in self.clusters[i]:
                self.alloc = cluster.resize(self.alloc, self.sliceSize)

            print("\nCut pizza:")
            for c in self.alloc:
                print(c)

            sum = 0
            for row in self.alloc:
                for el in row:
                    if el != 0:
                        sum += 1

            self.results.append(sum)
            print("Covered ", sum, " cells out of ", self.sizeX*self.sizeY)

            i += 1

    def _cut(self, window, i):
        while window.moveRight():
            cluster = window.getCluster(len(self.clusters[0])+1)
            if cluster is not None:
                self.clusters[i].append(cluster)
            #print("move right")

        if window.moveDown():
            self._cut(window, i)
        else :
            return "Done"



    #def allocateClusters(self, window):
     #   window.getCluster

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
        print("Pizza: ")
        for line in file:
            line = line.replace("\n"," ").replace("T", "0 ").replace("M", "1 ").strip(" ").split(" ")
            print(line)
            col = 0
            for ing in line:
                self.pizza[row][col] = int(ing)
                col += 1

            row += 1

    def _initWindows(self):
        cells1 = [[0,0],[1,0]]
        self.windows.append(Window(cells1, self.sizeX, self.sizeY, self.pizza, self.countIng))

        cells = [[self._getPoint(x,y) for x in range(2)] for y in range(self.countIng*2)]
        self.windows.append(Window(cells, self.sizeX, self.sizeY, self.pizza, self.countIng))

        self.results.append(None)
        self.results.append(None)

    def _getPoint(self, x, y):
        if x == 0:
            return y%self.countIng
        if x == 1:
            return y//self.countIng



#
#
#
class Cluster(object):

    cells = None
    num = 1

    def __init__(self, cells, num):
        self.cells = copy.deepcopy(cells)
        self.num = num

    def resize(self, allocArea, sliceSize):
        allocArea = self._resize(allocArea,sliceSize)
        return allocArea


    def _resize(self, allocArea, sliceSize):

        new_cells = self._canResizeRight(allocArea, sliceSize)
        if new_cells is not None:
            for nc in new_cells:
                allocArea[nc[0]][nc[1]] = self.num
                self.cells.append(nc)
            self._resize(allocArea, sliceSize)

        new_cells = self._canResizeDown(allocArea, sliceSize)
        if new_cells is not None:
            for nc in new_cells:
                allocArea[nc[0]][nc[1]] = self.num
                self.cells.append(nc)
            self._resize(allocArea, sliceSize)

        new_cells = self._canResizeLeft(allocArea, sliceSize)
        if new_cells is not None:
            for nc in new_cells:
                allocArea[nc[0]][nc[1]] = self.num
                self.cells.append(nc)
            self._resize(allocArea, sliceSize)

        new_cells = self._canResizeUp(allocArea, sliceSize)
        if new_cells is not None:
            for nc in new_cells:
                allocArea[nc[0]][nc[1]] = self.num
                self.cells.append(nc)
            self._resize(allocArea, sliceSize)

        return allocArea


    def _canResizeRight(self, allocArea, sliceSize):
        _, _, row, col = self.minMaxRowCol()
        newCells = self._resizeRight(col)
        return self.noneOrCells(newCells, allocArea, sliceSize)

    def _canResizeDown(self, allocArea, sliceSize):
        _, _, row, col = self.minMaxRowCol()
        newCells = self._resizeDown(row)
        return self.noneOrCells(newCells, allocArea, sliceSize)

    def _canResizeLeft(self, allocArea, sliceSize):
        row, col, _, _ = self.minMaxRowCol()
        newCells = self._resizeLeft(col)
        return self.noneOrCells(newCells, allocArea, sliceSize)

    def _canResizeUp(self, allocArea, sliceSize):
        row, col, _, _ = self.minMaxRowCol()
        newCells = self._resizeUp(row)
        return self.noneOrCells(newCells, allocArea, sliceSize)


    def noneOrCells(self, newCells, allocArea, sliceSize):
        if len(newCells)+len(self.cells) > sliceSize:
            return None

        for new_cell in newCells:
            try:
                if allocArea[new_cell[0]][new_cell[1]] != 0:
                    return None
            except IndexError:
                return None

        if len(newCells) == 0:
            return None

        return newCells


    def _resizeRight(self, maxCol):
        return self._resizeDirection(1, 1, maxCol)

    def _resizeDown(self, maxRow):
        return self._resizeDirection(0, 1, maxRow)

    def _resizeLeft(self, minCol):
        return self._resizeDirection(1, -1, minCol)

    def _resizeUp(self, minRow):
         return self._resizeDirection(0, -1, minRow)

    def _resizeDirection(self, index, inc, col_row):
        cells = copy.deepcopy(self.cells)
        new_cells = []
        for c in cells:
            if c[index] == col_row:
                c[index] += inc
                if c[index] >= 0:
                    new_cells.append(c)
        return new_cells

    def minMaxRowCol(self):
        minRow = 5000
        minCol = 5000
        maxRow = 0
        maxCol = 0

        for c in self.cells:
            if c[0] > maxRow:
                maxRow = c[0]
            if c[0] < minRow:
                minRow = c[0]
            if c[1] > maxCol:
                maxCol = c[1]
            if c[1] < minCol:
                minCol = c[1]

        return minRow, minCol, maxRow, maxCol

#
#
#
class Window(object):

    cells = None
    sizeX = 0
    sizeY = 0
    pizza = None
    countIng = 0
    alloc = []
    clusterCount = 0

    def __init__(self, cells, sizeX, sizeY, pizza, countIng):
        self.cells = cells
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.pizza = pizza
        self.countIng = countIng
        #self.alloc = [[0 for x in range(self.sizeY)] for y in range(self.sizeX)]

    def moveDown(self):
        if self._canMoveDown():
            for cell in self.cells:
                cell[0] += 1

            return True
        else:
            return False

    def moveRight(self):
        if self._canMoveRight():
            for cell in self.cells:
                cell[1] += 1

            return True
        else:
            delta = self.cells[0][1]
            for cell in self.cells:
                cell[1] -= delta
            return False

    #
    #
    #
    def _hasCluster(self):

        for cell in self.cells:
            if self.alloc[cell[0]][cell[1]] != 0:
                return False

        sum = 0
        for cell in self.cells:
            sum += self.pizza[cell[0]][cell[1]]

        if sum == self.countIng:
            self.clusterCount += 1
            for cell in self.cells:
                self.alloc[cell[0]][cell[1]] = self.clusterCount
            return True

        return False

    #
    #
    #
    def getCluster(self, i):
        if self._hasCluster():
             return Cluster(self.cells, i)

        return None

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
def main():
    p = Pizza("small.in")
    p.cut()

if __name__ == '__main__':
    main()
