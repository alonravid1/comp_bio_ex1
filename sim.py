import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import rv_discrete


class Simulation:
    
    def __init__(self, p, l, s1, s2, s3, s4, iterations=100, shape=(100,100)):
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
        
    
    def run(self, preprocess = False):
        """
        runs the simulation using the class's set attributes.
        returns a numpy array where each index holds the lattice's
        got_rumour value in the respective iteration.
        """
        if preprocess:
            frames = np.ndarray(shape=(self.iterations,100,100), dtype=self.features)
            for i in range (self.iterations):
                self.simulate_step()
                # save rumour spreading matrix 
                frames[i] = self.lattice
                
                # this is used to check the sim without the gui:
                # plt.title(f"iteration number {i}")
                # plt.imshow(self.lattice['got_rumour'])
                # plt.pause(0.02)
            return frames
        else:
            self.simulate_step()
            return self.lattice


        
            
    def create_cell_lattice(self):
        """
        create a new lattice graph of people with random assignments according
        to the given distribution parameters
        """
        self.features = np.dtype([('exists', 'bool'), ('sus_level', 'f8'), ('heard_rumour','i4'),('cooldown','i4'),('got_rumour', 'i4')])
        self.lattice = np.ndarray(shape=self.shape, dtype=self.features)
        
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
        
    def simulate_step(self):
        """
        run one iteration of the simulation
        """
        # remove influence of the previous iteration, done
        # here to allow frame to aputre rumour spread
        self.lattice['heard_rumour'] = np.zeros(self.shape)
        
        # spread rumour and reduce cooldown
        # based on the previous iteration
        it_spread = np.nditer(self.lattice, flags=['multi_index'], op_flags=['readwrite'])
        for cell in it_spread:
            if not cell['exists']:
            # no person in lattice cell
                continue
            
            # person has decided to spread the rumour last iteration
            if cell['cooldown'] == self.l:
                self.spread_rumour(*it_spread.multi_index)
                
                # current iteration counts towards rumour spreaded
                cell['cooldown'] -= 1

            # person has spread the rumour in the last l iterations               
            elif cell['cooldown'] > 0:
                cell['cooldown'] -= 1
        
        # decide to spread rumour based on the previous iteration
        it_decide = np.nditer(self.lattice, flags=['multi_index'], op_flags=['readwrite'])
        for cell in it_decide:
            if cell['cooldown'] > 0:
                continue
            """
            decide whether or not to pass on the rumour
            based on a number sampled uniformly at random
            between 0 and 1, and according to susceptibility and
            whether or not the cell heard the rumour at least twice in
            the past iteration
            """
            if (cell['heard_rumour'] == 1 and
                                np.random.rand(1) < cell['sus_level']):
                cell['cooldown'] = self.l
            elif (cell['heard_rumour'] > 1 and
                            np.random.rand(1) < cell['sus_level'] + 1/3):
                cell['cooldown'] = self.l
            else:
                # cell has not heard rumour and will not spread it
                pass

    def get_stats(self):
        heard_rumour = 0
        it_spread = np.nditer(self.lattice)
        for cell in it_spread:
            if not cell['exists']:
            # no person in lattice cell
                continue
            if cell['got_rumour'] > 0:
                heard_rumour += 1
        percent_heard = heard_rumour / (self.shape[0]*self.shape[1])
        return percent_heard

                    
                    



if __name__ == '__main__':
    # pop density parameter
    p = 0.85

    # rumour spreading cooldown parameter
    l = 5

    # num of iterations parameter
    iterations = 100

    # susceptibility level probability parameters
    s1 = 0.7
    s2 = 0.15
    s3 = 0.1
    s4 = 0.05
    raw_sim_values = [p, l, s1, s2, s3, s4, iterations]
    sim_values = [round(i, 2) for i in raw_sim_values]
   

    # sim = Simulation(0.7, 2, 15, 0.7, 0.15, 0.1, 0.05)
    average_spread = 0
    repeats = 30
    for i in range(repeats):
        sim = Simulation(*sim_values)
        sim.run(preprocess=True)
        average_spread += sim.get_stats()
    average_spread = average_spread/repeats
    print(average_spread)
    
        