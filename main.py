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

    for i in range(0, 100, 5):
        for j in range(0, 100, 5):
            lattice[i:i+3, j:j+3]['sus_level'] = 1
            lattice[i+3, j:j+5]['sus_level'] = 1/3
            lattice[i:i+5, j+3]['sus_level'] = 1/3
            lattice[i+4, j:j+5]['sus_level'] = 1/3
            lattice[i:i+5, j+4]['sus_level'] = 1/3

    # for i in range(5, 100, 6):
    #     lattice[:, i:i+5]['sus_level'] = np.array([2/3, 2/3, 2/3, 2/3, 2/3])

    lattice['heard_rumour'] = np.zeros(shape)
    lattice['cooldown'] = np.zeros(shape)
    lattice['got_rumour'] = np.zeros(shape)

    return lattice



def generate_dist_stats(distributions, p, l , iterations=100, repeats = 15, stats_samples = 20):
    """generate graph of spread rate per iteration for all distributions given.
    the sample rate is set by the stats_samples argument divided by the iterations argument.

    Args:
        distributions (array): array of distributions of susceptibilty levels.
        p (float): portion of existing cells
        l (int): number of iterations cooldown on spreading a rumour
        iterations (int, optional): number of iterations. Defaults to 100.
        repeats (int, optional): number of times the simulation is run per parameter value. Defaults to 15.
        stats_samples (int, optional): how many samples should be taken during the simulation. Defaults to 20.
    """
    stats_sr = iterations//stats_samples
    dist_results = np.zeros((len(distributions), stats_samples))
    dist_labels = []
    for dist in range(len(distributions)):
        average_spread = np.zeros(stats_samples)
        distributions[dist] = check_sum(*distributions[dist])
        sim_values = [p, l, *distributions[dist], iterations]

        for i in range(repeats):
            sim = Sim.Simulation(*sim_values)
            frames, stats = sim.run(preprocess=True, stats_sr=stats_sr)
            for i in range(0, stats_samples):
                average_spread[i] += stats[i]

        average_spread = average_spread/repeats
        dist_results[dist] = average_spread

        dist_labels.append(f'distribution: {dist+1}; STD: {round(np.std(dist_results[dist]),3)}')
        
    draw_graph(stats_samples, dist_results, dist_labels, "Distributions Spread Rate")


def generate_L_stats(upper_limit, p, dist, iterations=100, repeats = 15, stats_samples = 20):
    """generate graph of spread rate per iteration for all L values between 2 and the upper limit.
    the sample rate is set by the stats_samples argument divided by the iterations argument.

    Args:
        upper_limit (int): upper limit of L value
        p (float): portion of existing cells
        dist (_type_): _description_
        iterations (int, optional): number of iterations. Defaults to 100.
        repeats (int, optional): number of times the simulation is run per parameter value. Defaults to 15.
        stats_samples (int, optional): how many samples should be taken during the simulation. Defaults to 20.
    """
    stats_sr = iterations//stats_samples
    limit_results = np.zeros((upper_limit - 2, stats_samples))
    limit_labels = []
    for l in range(2,upper_limit):
        average_spread = np.zeros(stats_samples)
        sim_values = [p, l, *dist, iterations]

        for i in range(repeats):
            sim = Sim.Simulation(*sim_values)
            frames, stats = sim.run(preprocess=True, stats_sr=stats_sr)
            for i in range(0, stats_samples):
                average_spread[i] += stats[i]

        average_spread = average_spread/repeats
        limit_results[l-2] = average_spread
        limit_labels.append(f"L={l}")

    draw_graph(stats_samples, limit_results, limit_labels, "L Spread Rates")

     


     
if __name__ == '__main__':
    gui = Gui.Gui(strategic_sim)
    gui.start()
    
    # # some default parmeters for intial testing
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

    # # # a regular simulation, will not print anything
    # # # sim = Sim.Simulation(*sim_values)

    # # create graphs for statistics on multiple runs per parameter value
    # distributions = [
    #     [0.7, 0.15, 0.1, 0.05], [0.6, 0.15, 0.1, 0.15],
    #     [0.6, 0.15, 0.15, 0.1], [0.5, 0.2, 0.15, 0.15],
    #     [0.5, 0.25, 0.15, 0.1], [0.4, 0.25, 0.2, 0.15],
    #     [0.4, 0.2, 0.2, 0.2], [0.4, 0.3, 0.2, 0.1],
    #     [0.3, 0.25, 0.2, 0.15], [0.3, 0.25, 0.25, 0.2]
    #     ]

    # # run one at a time
    # generate_dist_stats(distributions, p, l,repeats=1)
    # plt.savefig("distributions_fig.png")

    # dist = [0.7, 0.15, 0.1, 0.05]
    # generate_L_stats(3, p, dist, repeats=1)
    # plt.savefig("L_fig.png")

    # # run strategic sim multiple times for statistics
    # average_spread = 0
    # for i in range(20):
    #     sim = Sim.Simulation(*sim_values, strategy=strategic_sim)
    #     sim.run(preprocess=True)
    #     average_spread += sim.get_stats()
    # average_spread = average_spread/20*100
    # print(average_spread)

