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
        

def draw_graph(stats_samples, results, labels, title):
    x = np.arange(stats_samples)
    x = x*5
    colors = []

    for i in range(stats_samples):
        colors.append('#%06X' % np.random.randint(0, 0xFFFFFF))
    graph = plt.figure()
    for i in range(len(results)):
        plt.plot(x, results[i], color=colors[i], label=labels[i])
    plt.xlabel("Iteration Number")
    plt.ylabel("Percentage Spread")
    plt.legend()
    plt.title(title)
    

def strategic_sim(shape=(100,100)):
    """
    creates a new lattice graph of people with random assignments according
    to the given distribution parameters.
    """
    features = np.dtype([('exists', 'bool'), ('sus_level', 'f8'), ('heard_rumour','i4'),('cooldown','i4'),('got_rumour', 'i4')])
    lattice = np.ndarray(shape=shape, dtype=features)
    
    # generate initial lattice, all cells exist and have susceptibilty level of 1
    lattice['exists'] = np.full(shape, True)
    lattice['sus_level'] = np.zeros(shape)

    for i in range(0, 100, 6):
        for j in range(0, 100, 6):
            lattice[i:i+5, j:j+5]['sus_level'] = 1

    # Add columns of [0, 0, 1, 0, 0] between each box
    for i in range(5, 100, 6):
        lattice[:, i:i+5]['sus_level'] = np.array([1/3, 1/3, 2/3, 1/3, 1/3])

    lattice['heard_rumour'] = np.zeros(shape)
    lattice['cooldown'] = np.zeros(shape)
    lattice['got_rumour'] = np.zeros(shape)

    return lattice
    

     
if __name__ == '__main__':
    gui = Gui.Gui(strategic_sim)
    gui.start()
    
    # # pop density parameter
    # p = 0.8

    # # rumour spreading cooldown parameter
    # l = 5

    # # num of iterations parameter
    # iterations = 100

    # # susceptibility level probability parameters
    # s1 = 0.7
    # s2 = 0.15
    # s3 = 0.1
    # s4 = 0.05
    # raw_sim_values = [p, l, s1, s2, s3, s4, iterations]
    # sim_values = [round(i, 2) for i in raw_sim_values]
   

    # # sim = Simulation(0.7, 2, 15, 0.7, 0.15, 0.1, 0.05)
    # repeats = 15
    # stats_samples = 20
    # stats_sr = iterations//stats_samples
    # # distributions = [
    # #     [0.7, 0.15, 0.1, 0.05], [0.6, 0.15, 0.1, 0.15],
    # #     [0.6, 0.15, 0.15, 0.1], [0.5, 0.2, 0.15, 0.15],
    # #     [0.5, 0.25, 0.15, 0.1], [0.4, 0.25, 0.2, 0.15],
    # #     [0.4, 0.2, 0.2, 0.2], [0.4, 0.3, 0.2, 0.1],
    # #     [0.3, 0.25, 0.2, 0.15], [0.3, 0.25, 0.25, 0.2]
    # #     ]
    
    # # dist_results = np.zeros((len(distributions), stats_samples))
    # # dist_labels = []
    # # for dist in range(len(distributions)):
    # #     average_spread = np.zeros(stats_samples)
    # #     distributions[dist] = check_sum(*distributions[dist])
    # #     sim_values = [p, l, *distributions[dist], iterations]

    # #     for i in range(repeats):
    # #         sim = Sim.Simulation(*sim_values)
    # #         frames, stats = sim.run(preprocess=True, stats_sr=stats_sr)
    # #         for i in range(0, stats_samples):
    # #             average_spread[i] += stats[i]

    # #     average_spread = average_spread/repeats
    # #     dist_results[dist] = average_spread

    # #     dist_labels.append(f'distribution: {dist+1}; STD: {round(np.std(dist_results[dist]),3)}')
    # # print(dist_results)
    
    # upper_limit = 10
    # limit_results = np.zeros((upper_limit - 2, stats_samples))
    # limit_labels = []
    # for l in range(2,upper_limit):
    #     average_spread = np.zeros(stats_samples)
    #     dist = [0.6, 0.15, 0.1, 0.15]
    #     sim_values = [p, l, *dist, iterations]

    #     for i in range(repeats):
    #         sim = Sim.Simulation(*sim_values)
    #         frames, stats = sim.run(preprocess=True, stats_sr=stats_sr)
    #         for i in range(0, stats_samples):
    #             average_spread[i] += stats[i]

    #     average_spread = average_spread/repeats
    #     limit_results[l-2] = average_spread
    #     limit_labels.append(f"L={l}")
    # print(limit_results)

    # fig, ax = plt.subplots(1,2)
    # # draw_graph(stats_samples, dist_results, dist_labels, "Distributions Spread Rate")
    # # plt.savefig("Distributions.png")
    # draw_graph(stats_samples, limit_results, limit_labels, "L Spread Rates")
    # plt.savefig("L.png")
