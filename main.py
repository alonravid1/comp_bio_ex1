import Sim
import Gui

def check_sum(self, s1, s2, s3, s4):
        """Check if 

        Args:
            s1 (_type_): _description_
            s2 (_type_): _description_
            s3 (_type_): _description_
            s4 (_type_): _description_

        Returns:
            _type_: _description_
        """
        diff = 1 - sum([s1, s2, s3, s4])
        s1 += diff
        return s1, s2, s3, s4
        
if __name__ == '__main__':
    gui = Gui.Gui()
    gui.start()
    
       # pop density parameter
    # p = 0.85

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
    # repeats = 5
    # raw_distributions = [
    #     [0.7, 0.15, 0.1, 0.05], [0.6, 0.15, 0.1, 0.15],
    #     [0.6, 0.15, 0.15, 0.1], [0.5, 0.2, 0.15, 0.15],
    #     [0.5, 0.25, 0.15, 0.1], [0.4, 0.25, 0.2, 0.15],
    #     [0.4, 0.2, 0.2, 0.2], [0.4, 0.3, 0.2, 0.1],
    #     [0.3, 0.25, 0.2, 0.15], [0.3, 0.25, 0.25, 0.2]
    #     ]
    
    # distributions = [round(i, 2) for i in raw_distributions]
    # results = []
    # for dist in distributions:
    #     average_spread = 0
    #     sim_values = [p, l, *dist, iterations]
    #     for i in range(repeats):
    #         sim = Simulation(*sim_values)
    #         sim.run(preprocess=True)
    #         average_spread += sim.get_stats()
    #     average_spread = average_spread/repeats
    #     results.append(average_spread)
    # print(results)