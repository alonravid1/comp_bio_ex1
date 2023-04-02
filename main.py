import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import rv_discrete


class Board:
    
    def __init__(self, p, sus_prob, l, shape=(100,100)) -> None:
        """
        set parameters to board, create a lattice graph of
        people represented by a tuple of:
        (existing, susceptibility level, has heard rumor, has passed rumor)
        which allow the simulation to check each Cell's status
        """
        self.p_dist = rv_discrete(values=([False, True], [(1-p), p]))
        self.sus_dist = rv_discrete(values=([1, 2/3, 1/3, 0 ], sus_prob))

        self.l = l
        self.shape = shape

        self.create_cell_lattice()
            
    def create_cell_lattice(self):
        """
        create a new lattice graph of people with random assignments according
        to the given distribution parameters
        """
        lattice = np.ndarray(shape=self.shape, dtype=[('exists', 'bool'), ('cell', Cell)])
        
        lattice['exists'] = self.p_dist.rvs(size=self.shape)

        # generate
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                lattice[i, j]['cell'] = Cell(self.sus_dist.rvs(size=1), self.l)
        
         # add neighbors to all cells
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                neighbors = []

                if i > 0 and lattice[i-1, j]['exists']:
                    neighbors.append(lattice[i-1, j]['cell'])

                if i < self.shape[0]-1 and lattice[i+1, j]['exists']:
                    neighbors.append(lattice[i+1, j]['cell'])

                if j > 0 and lattice[i, j-1]['exists']:
                    neighbors.append(lattice[i, j-1]['cell'])

                if j < self.shape[1]-1 and lattice[i, j+1]['exists']:
                    neighbors.append(lattice[i, j+1]['cell'])

                lattice[i, j]['cell'].add_neighbors(neighbors)
        self.lattice = lattice

    def plot_lattice(self):
        """
        plot the lattice as a matrix image with regard to the specified cell field
        """
        plt.imshow(self.lattice["cell"]., cmap='viridis')
        plt.colorbar()
        plt.show()


    
    def pass_rumor(self):
        # get random indices within the matrix
        initial_x = np.random.randint(low=0, high=self.shape(0))
        initial_y = np.random.randint(low=0, high=self.shape(1))

class Cell:

    def __init__(self, sus_level, l):
        self.base_sus_level = sus_level
        self.temp_sus_level = sus_level
        self.l = l
        self.heard_rumour = 0
        self.passed_rumour = 0
        self.neighbours = None
    
    def add_neighbors(self, neighbours):
        self.neighbours = neighbours
    
    def get_sus(self):
        return self.base_sus_level
    
    def pass_rumour(self):
        self.heard_rumour += 1

        # has passed the rumour less than l iterations ago
        if self.passed_rumour > 0:
           self.passed_rumour -= 1
           return
        
        # has heard rumour from multiple neighbours
        if self.heard_rumour >= 2:
           self.temp_sus_level = self.base_sus_level + 1/3

        # has decided to pass the rumour along
        if np.random.rand(1) < self.temp_sus_level:
            for neighbour in self.neighbours:
               neighbour.pass_rumour()   
            self.passed_rumour = self.l
        
        # reset susceptibility level
        self.temp_sus_level = self.base_sus_level

if __name__ == '__main__':
    # pop density parameter
    p = 0.4 

    # susceptibility level probability parameters
    s1 = 0.1
    s2 = 0.3
    s3 = 0.5
    s4 = 0.1
    sus_prob = [s1, s2, s3, s4]

    l = 2
    b = Board(p, sus_prob, l)
    b.plot_lattice()
        