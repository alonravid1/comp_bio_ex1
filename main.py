import Sim
import Gui
import numpy as np
import matplotlib.pyplot as plt

def check_sum(s1, s2, s3, s4):
        """check if an arbitrary set of distribution values
        add up to 1, if not add the tiny difference to s1

        Args:
            s1 (float): level one susceptibility portion
            s2 (float): level two susceptibility portion
            s3 (float): level three susceptibility portion
            s4 (float): level four susceptibility portion

        Returns:
            the same distribution, with any floating point error
            added to s1 so the probabilites add up to 1
        """
        diff = 1 - sum([s1, s2, s3, s4])
        s1 += diff
        return s1, s2, s3, s4
        
if __name__ == '__main__':
    # gui = Gui.Gui()
    # gui.start()
    
    # pop density parameter
    p = 0.8

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
    repeats = 1
    distributions = [
        [0.7, 0.15, 0.1, 0.05], [0.6, 0.15, 0.1, 0.15]
        # [0.6, 0.15, 0.15, 0.1], [0.5, 0.2, 0.15, 0.15],
        # [0.5, 0.25, 0.15, 0.1], [0.4, 0.25, 0.2, 0.15],
        # [0.4, 0.2, 0.2, 0.2], [0.4, 0.3, 0.2, 0.1],
        # [0.3, 0.25, 0.2, 0.15], [0.3, 0.25, 0.25, 0.2]
        ]
    
    dist_results = np.zeros((len(distributions), 20))
    for dist in range(len(distributions)):
        average_spread = np.zeros(20)
        distributions[dist] = check_sum(*distributions[dist])
        sim_values = [p, l, *distributions[dist], iterations]

        for i in range(repeats):
            sim = Sim.Simulation(*sim_values)
            frames, stats = sim.run(preprocess=True)
            for i in range(0, 20):
                average_spread[i] += stats[i]

        average_spread = average_spread/repeats
        dist_results[dist] = average_spread
    print(dist_results)

    limit_results = np.zeros((1, 20))
    for l in range(2,3):
        average_spread = np.zeros(20)
        dist = [0.7, 0.15, 0.1, 0.05]
        sim_values = [p, l, *dist, iterations]

        for i in range(repeats):
            sim = Sim.Simulation(*sim_values)
            frames, stats = sim.run(preprocess=True)
            for i in range(0, 20):
                average_spread[i] += stats[i]

        average_spread = average_spread/repeats
        limit_results[l-1] = average_spread
    print(limit_results)

x = np.arange(20)
plt.plot(x, dist_results, color='b', label='distributions')
plt.plot(x, limit_results, color='r', label='distributions')
