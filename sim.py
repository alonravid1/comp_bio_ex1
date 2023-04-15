import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import rv_discrete


class Simulation:
    
    def __init__(self, p, l, iterations, s1, s2, s3, s4, shape=(100,100)):
        """
        set parameters to board, create a lattice graph of
        people represented by a tuple of:
        (existing, susceptibility level, has heard rumor, has passed rumor)
        which allow the simulation to check each Cell's status
        """
        if p == 0 :
            exit(-1)

        self.p_dist = rv_discrete(values=([False, True], [(1-p), p]))
        self.sus_dist = rv_discrete(values=([1, 2/3, 1/3, 0 ], [s1, s2, s3, s4]))

        self.l = l
        self.shape = shape
        self.iterations = iterations
        self.create_cell_lattice()
        
        initial_x = np.random.randint(low=0, high=self.shape[0])
        initial_y = np.random.randint(low=0, high=self.shape[1])

        # get random indices within the matrix, where a preson exists
        while not self.lattice[initial_x, initial_y]['exists']:
            initial_x = np.random.randint(low=0, high=self.shape[0])
            initial_y = np.random.randint(low=0, high=self.shape[1])

        # initial_x = self.shape[0]//2
        # initial_y = self.shape[1]//2

        # set initial spreader
        self.lattice[initial_x, initial_y]['cooldown'] = self.l
        
    
    def run(self):
        """
        runs the simulation using the class's set attributes.
        returns a numpy array where each index holds the lattice's
        got_rumour value in the respective iteration.
        """
        frames = np.ones((self.iterations, self.shape[0], self.shape[1]))

        for i in range (self.iterations):
            self.simulate_step()
            # save rumour spreading matrix 
            frames[i]= self.lattice['got_rumour']
            
            # this is used to check the sim without the gui:
            # plt.title(f"iteration number {i}")
            # plt.imshow(self.lattice['got_rumour'])
            # plt.pause(0.02)
        return frames
        
            
    def create_cell_lattice(self):
        """
        create a new lattice graph of people with random assignments according
        to the given distribution parameters
        """
        features = np.dtype([('exists', 'bool'), ('sus_level', 'i4'), ('heard_rumour','i4'),('cooldown','i4'),('got_rumour', 'i4')])
        self.lattice = np.ndarray(shape=self.shape, dtype=features)
        
        # generate
        self.lattice['exists'] = self.p_dist.rvs(size=self.shape)
        self.lattice['sus_level'] = self.sus_dist.rvs(size=self.shape)
        self.lattice['heard_rumour'] = np.zeros(self.shape)
        self.lattice['cooldown'] = np.zeros(self.shape)
        self.lattice['got_rumour'] = np.zeros(self.shape)
        

    def spread_rumour(self, i, j):
        """
        this function is called when a cell decides to spread a rumour,
        it adds 1 to each neighbour's heard_rumour attribute
        """
        
        # if is split to prevent errors when at lattice's edge
        if i > 0:
            if self.lattice[i-1, j]['exists']:
                self.lattice[i-1, j]['heard_rumour'] += 1

        if i < self.shape[0]-1:
            if self.lattice[i+1, j]['exists']:
                self.lattice[i+1, j]['heard_rumour'] += 1

        if j > 0:
            if self.lattice[i, j-1]['exists']:
                self.lattice[i, j-1]['heard_rumour'] += 1

        if j < self.shape[1]-1:
            if self.lattice[i, j+1]['exists']:
                self.lattice[i, j+1]['heard_rumour'] += 1

        self.lattice[i, j]['got_rumour'] += 1
        
    def make_decision(self, i, j):
        """
        decide whether or not to pass on the rumour
        based on a number sampled uniformly at random
        between 0 and 1, and according to susceptibility and
        whether or not the cell heard the rumour at least twice in
        the past iteration
        """
        # person has yet decided to spread the rumour
        if self.lattice[i, j]['heard_rumour'] == 1:
            # person heard it once
            if np.random.rand(1) < self.lattice[i, j]['sus_level']:
                # decide whether or not to spread the rumour
                self.lattice[i, j]['cooldown'] = self.l
                return # decided to spread, will do so next iteration
        
        elif self.lattice[i, j]['heard_rumour'] >= 2:
            # person heard it twice
            if np.random.rand(1) < self.lattice[i, j]['sus_level'] + 1/3:
                # decide whether or not to spread the rumour
                self.lattice[i, j]['cooldown'] = self.l
                return # decided to spread, will do so next iteration

        else:
            # person has not heard the rumour at all
            return
            
    def simulate_step(self):
        """
        run one iteration of the simulation
        """
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
                    self.lattice[i, j]['cooldown'] -= 1
                
                # once a decision has been made for the next iteration,
                # remove influence of the previous one
                self.lattice[i, j]['heard_rumour'] = 0
                    



if __name__ == '__main__':
    # pop density parameter
    p = 0.8

    # rumour spreading cooldown parameter
    l = 2

    # num of iterations parameter
    iterations = 100

    # susceptibility level probability parameters
    s1 = 0.9
    s2 = 0.1
    s3 = 0
    s4 = 0

    # sim = Simulation(p, l, iterations, s1, s2, s3, s4)

    sim = Simulation(0.7, 2, 15, 0.7, 0.15, 0.1, 0.05)
    frames = sim.run()
    
        