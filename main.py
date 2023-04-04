import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import rv_discrete


class Simulation:
    
    def __init__(self, p, sus_prob, l, iterations, shape=(100,100)):
        """
        set parameters to board, create a lattice graph of
        people represented by a tuple of:
        (existing, susceptibility level, has heard rumor, has passed rumor)
        which allow the simulation to check each Cell's status
        """
        if p == 0 :
            exit(-1)

        self.p_dist = rv_discrete(values=([False, True], [(1-p), p]))
        self.sus_dist = rv_discrete(values=([1, 2/3, 1/3, 0 ], sus_prob))

        self.l = l
        self.shape = shape

        self.create_cell_lattice()
        
        initial_x = np.random.randint(low=0, high=self.shape[0])
        initial_y = np.random.randint(low=0, high=self.shape[1])

        # get random indices within the matrix, where a preson exists
        while not self.lattice[initial_x, initial_y]['exists']:
            initial_x = np.random.randint(low=0, high=self.shape[0])
            initial_y = np.random.randint(low=0, high=self.shape[1])

        # set initial spreader
        self.lattice[initial_x, initial_y]['spread_rumour'] = self.l

        for i in range (iterations):
            self.simulate_step()
            
    def create_cell_lattice(self):
        """
        create a new lattice graph of people with random assignments according
        to the given distribution parameters
        """
        features = np.dtype([('exists', 'bool'), ('sus_level', 'i4'), ('heard_rumour','i4'),('cooldown','i4')('spread_rumour', 'i4')])
        self.lattice = np.ndarray(shape=self.shape, dtype=features)
        
        # generate
        self.lattice['exists'] = self.p_dist.rvs(size=self.shape)
        self.lattice['sus_level'] = self.sus_dist.rvs(size=self.shape)
        self.lattice['heard_rumour'] = np.zeros(self.shape)
        self.lattice['cooldown'] = np.zeros(self.shape)
        self.lattice['spread_rumour'] = np.zeros(self.shape)
        

    def spread_rumour(self, i, j):
        if i > 0 and self.lattice[i-1, j]['exists']:
            self.lattice[i-1, j]['heard_rumour'] += 1

        if i < self.shape[0]-1 and self.lattice[i+1, j]['exists']:
            self.lattice[i+1, j]['heard_rumour'] += 1

        if j > 0 and self.lattice[i, j-1]['exists']:
            self.lattice[i, j-1]['heard_rumour'] += 1

        if j < self.shape[1]-1 and self.lattice[i, j+1]['exists']:
            self.lattice[i, j+1]['heard_rumour'] += 1

        self.lattice[i, j]['spread_rumour'] += 1
        
    def make_decision(self, i, j):
        # person has yet decided to spread the rumour
        if self.lattice[i, j]['heard_rumour'] == 1:
        # person heard it once
            if np.random.rand(1) < self.lattice[i, j]['sus_level']:
                # decide whether or not to spread the rumour
                self.lattice[i, j]['spread_rumour'] = self.l
                return # decided to spread, will do so next iteration
        
        elif self.lattice[i, j]['heard_rumour'] >= 2:
            # person heard it twice
            if np.random.rand(1) < self.lattice[i, j]['sus_level'] + 1/3:
                # decide whether or not to spread the rumour
                self.lattice[i, j]['spread_rumour'] = self.l
                return # decided to spread, will do so next iteration

        else:
            # person has not heard the rumour at all
            return
            
    def simulate_step(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if not self.lattice[i, j]['exists']:
                # no person in lattice cell
                    continue
                
                # person has decided to spread the rumour last iteration
                if self.lattice[i, j]['cooldown'] == self.l:
                    self.spread_rumour(i, j)
                    
                    # current iteration counts towards rumour spreaded
                    self.lattice[i, j]['cooldown'] -= 1

                # person hasn't spread the rumour for at least
                # l iterations
                elif self.lattice[i, j]['cooldown'] == 0:
                    self.make_decision(i, j)

                # person has spread the rumour in the last l iterations               
                else:
                    self.lattice[i, j]['spread_rumour'] -= 1
                
                # once a decision has been made for the next iteration,
                # remove influence of the previous one
                self.lattice[i, j]['heard_rumour'] = 0
                    
                    


    def plot_lattice(self):
        """
        plot the lattice as a matrix image with regard to the specified cell field
        """
        values = self.lattice['heard_rumour']


        print(values)
        plt.imshow(values, cmap='viridis')
        plt.colorbar()
        plt.show()

                
                



if __name__ == '__main__':

    # pop density parameter
    p = 0.8

    # rumour spreading cooldown parameter
    l = 3

    # num of iterations parameter
    iterations = 10

    # susceptibility level probability parameters
    s1 = 0.3
    s2 = 0.3
    s3 = 0.2
    s4 = 0.2
    sus_prob = [s1, s2, s3, s4]

    sim = Simulation(p, sus_prob, l, iterations)
    sim.plot_lattice()
        