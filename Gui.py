import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import Sim
import time
import os


class Gui:
    def __init__(self, strategy=None):
        """initialise the GUI, start the main loop and show main screen

        Args:
            strategy (function, optional): a strategy function, which generates a lattice of cells
            according to a strategy and returns it, used inside the strategic simulation.
        """        
        
        # setting general GUI properties
        sg.theme('DarkAmber')
        
        self.AppFont = 'Any 14' # font
        self.shape = (500, 500) # size of simulation presented to user, not simulation dimensions!
        self.matrix_shape = (100,100)
        self.visuals = 'cooldown' # visualisation type, default is cooldown
        self.strategy = strategy

        # set main window's layout
        self.main_layout = [
            [sg.Button('Information', font=self.AppFont)],
            # set parameters
            [sg.Text('Enter parameters:', font='Any 18')],
            [sg.Text('P:',font=self.AppFont), sg.Input(key='p', size=(15,1), font=self.AppFont, default_text='0.85')],
            [sg.Text('L:',font=self.AppFont), sg.Input(key='l', size=(15,1), font=self.AppFont, default_text='5')],
                    
            [sg.Text('Number of Iterations:', font=self.AppFont),
                sg.Input(key='iter', size=(15,1), font=self.AppFont, default_text='100')],
            
            [sg.Text('Susceptibility Levels Distribution:', font=self.AppFont)],
            
            [sg.Text('S1',font=self.AppFont), sg.Input(key='s1', size=(15,1), font=self.AppFont, default_text='0.7'),
             sg.Text('S2',font=self.AppFont), sg.Input(key='s2', size=(15,1), font=self.AppFont, default_text='0.15'),
             sg.Text('S3',font=self.AppFont), sg.Input(key='s3', size=(15,1), font=self.AppFont, default_text='0.1'),
             sg.Text('S4',font=self.AppFont), sg.Input(key='s4', size=(15,1), font=self.AppFont, default_text='0.05')
            ],
            
            # set visualisation type
            [sg.Text('Visualisation Type', font=self.AppFont),
              sg.Button('Spread Cooldown', font=self.AppFont, disabled=True),
              sg.Button('Rumour Heard', font=self.AppFont),
              sg.Button('Times Rumour Heard', font=self.AppFont),
              sg.Button('None', font=self.AppFont)],
            
            # run different kinds of simulation
            [sg.Button('Start Simulation', font=self.AppFont)],

            [sg.Text('Generate Statistics:', font='Any 18')],
            [sg.Text('Number of Repeats:',font=self.AppFont),
             sg.Input(key='repeats', size=(15,1), font=self.AppFont, default_text='30')],
            [sg.Button('Generate Statistics', font=self.AppFont)],

            
            [sg.Button('Strategic Simulation', font=self.AppFont)],
            [sg.Button('Exit', font=self.AppFont)]
            ]
        
        self.infotext = """Welcome to the rumour spreading simulator.

Please enter the following parameters as follows:
* P - Portion of the cells that are inhibited. Enter a number between 0 and 1.
* L - Spread limiter, after spreading the rumour a cell cannot spread it again for L iterations. Enter a positive integer.
* Number of Iterations - How many iterations the simulation will run. Enter a positive integer.
* Susceptibilty Level Ratios - Each cell has a susceptibilty level between 1 to 4, where S1 means it will believe and spread every rumour it hears, S2 means he will believe and spread it with probabilty of 2/3, S3 with probabilty of 1/3 and 4 with probabilty of 0. The parameters S1 to S4 determine the ratio of cells with the respective susceptibilty level.
Enter 4 fractions summing up to a total of 1.

Visualisation types:
* Spread Cooldown - Color cells by how many iterations remain until it can spread the rumour again. A cell which spreads the rumour becomes bright and fades until it can spread it again.
* Rumour Heard - Colors cells by whether or not they have heard the rumour.
* Times Rumour Heard - Colors cells by how many times they have heard the rumour throughout the simulation.

Generate Statistics:
Set the number of repetitions, the simulation the runs for that number of times without visualisation, and then writes the average spread in a popup window.

Strategic Simulation:
Runs the simulation with a predefined strategy.
"""
        
    def create_sim_layout(self):
        """
        generates a simulation screen layout.
        the gui package cannot reuse a layout, generating a new
        layout with new element objects is the solution, rather
        than trying to create a template and starting to work on
        deep copying the very flexible nested arrays of elements.
        """
        fresh_layout = [
                    [sg.Text(key="show_iter", font='any 18'), sg.Text(key="stats", font='any 18')],
                    [sg.Image(key='frame')]
                    ]
        
        return fresh_layout
        
           
    def draw_frame(self, window, frame, iteration, stats):
        """
        function resizes the given frame to be bigger, saves it
        as an image and then shows it on the GUI for 0.05 of a second

        Args:
            window (sg.Window): a pysimplegui window
            frame (ndarray): a simulation lattice
            iteration (int): current iteration number
            stats (float): percentage of population which has heard the rumour
        """        
        
        resized_frame = np.ndarray(shape=self.shape)
        horizental_side = int(self.shape[0]/self.matrix_shape[0])
        vercitcal_side = int(self.shape[1]/self.matrix_shape[1])
        
        for i in range(0, self.shape[0]-horizental_side, horizental_side ):
            for j in range(0, self.shape[1]-vercitcal_side, vercitcal_side):
                # Draw the matrix on the graph
                resized_frame[i:i+horizental_side, j:j+vercitcal_side] = frame[int(i/horizental_side), int(j/vercitcal_side)]
        
        if self.visuals == 'heard rumour':
            vis_colors = 'seismic'
        else:
            vis_colors = 'magma'
        plt.imsave("frame.png", resized_frame, cmap=vis_colors)

        try:
            window['show_iter'].update(f"Iteration number: {iteration+1}")
            window['stats'].update(f"Percent heard: {round(stats*100, 2)}%")
            window['frame'].update("frame.png")
            # set window to middle of screen
            screen_width, screen_height = window.get_screen_dimensions()
            win_width, win_height = window.size
            x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
            window.move(x, y)
        except:
            # delete frame file
            try:
                os.remove("frame.png")
            except:
                pass


    def start_simulation(self, sim_values, strategy):
        """
        creates the new simulation window, runs the simulation
        to get all itertion frames, and then show each one
        using draw_frame(), afterwhich it gives the user the option to
        close the window whenever they'd like

        Args:
            sim_values (nparray): array of the simulation parameters
        """        

        window = sg.Window('Rumour Spreading Simulation',
                                    self.create_sim_layout(),
                                    finalize=True,
                                    resizable=True,
                                    element_justification="left")
        
        simulation = Sim.Simulation(*sim_values, strategy=strategy)
        iterations = sim_values[-1]
        event = 'initial value'

        if self.visuals == 'None':
            frames = simulation.run(preprocess=True)
            stats = simulation.get_stats()
            self.draw_frame(window, frames[iterations-1]['got_rumour'], iterations-1, stats)

            while event != sg.WIN_CLOSED:
                event, values = window.read(timeout=200)

            window.close()

            # delete frame file
            try:
                os.remove("frame.png")
            except:
                pass
            # sim closed and frame deleted, stop function
            return


        # draw first frame and then move the
        # window to the middle of the screen
        frame = simulation.run()

        if self.visuals == 'heard rumour':
            frame = (frame['got_rumour']>=1)*1
        else:
            frame = frame[self.visuals]
        
        stats = 0
        self.draw_frame(window, frame, 0, stats)
        event, values = window.read(timeout=2)

        # draw the simulation frames
        for i in range(1, iterations):
            frame = simulation.run()

            if self.visuals == 'heard rumour':
                frame = (frame['got_rumour']>=1)*1
            else:
                frame = frame[self.visuals]


            if i % 5 == 0 or i == (iterations-1):
                # update every 5 steps and at the end to speed the sim up
                stats = simulation.get_stats()
            
            # if rendering is fast, prevent instant presentation of all frames
            time.sleep(0.03)
            self.draw_frame(window, frame, i, stats)
            event, values = window.read(timeout=2)
            if event == sg.WIN_CLOSED:
                window.close()
                # delete frame file
                try:
                    os.remove("frame.png")
                except:
                    pass
                # sim closed and frame deleted, stop function
                return
            

        while event != sg.WIN_CLOSED:
            event, values = window.read(timeout=200)

        window.close()

        # delete frame file
        try:
            os.remove("frame.png")
        except:
            pass

        
    def process_values(self, values):
        """_summary_

        Args:
            values (nparray): array of simulation parameters as entered by the user

        Returns:
            nparray: an array of rounded values, confirming to the parameters conditions
        """        
        try:
            raw_sim_values = [float(values['p']), int(values['l']),
                        float(values['s1']), float(values['s2']),
                        float(values['s3']), float(values['s4']), int(values['iter'])]
            
            sim_values = [round(i, 2) for i in raw_sim_values]
            
            # check all values are positive
            if any(value < 0 for value in sim_values):
                sg.popup('Values cannot be negative')
                return None
            if (sim_values[1] < 1 or sim_values[-1] < 1):
                sg.popup('both L and number of iterations must be at least 1')
                return None
            if sum(sim_values[2:-1]) != 1 :
                sg.popup('distribution probability values must add up to 1')
                return None
            if sim_values[0] > 1 :
                sg.popup('P value must be between 0 and 1')
                return None
            
            return sim_values
        
        except:
            sg.popup('Error parsing input')
            return None
                

        


    def start(self):
        """
        starts the main window in which the parameters are set,
        allows multiple simulations to run and to change the parameters
        for each one without having to close the program
        """
        self.window = sg.Window('Rumour Spreading Simulation',
                                    self.main_layout,
                                    finalize=True,
                                    resizable=True,
                                    element_justification="left")
        # MAIN LOOP
        while True:
            event, values = self.window.read(timeout=200)
           
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if event == 'Spread Cooldown':
                # set visualisation type to cooldown, disable its button
                self.visuals = 'cooldown'
                self.window['Spread Cooldown'].update(disabled=True)
                self.window['Rumour Heard'].update(disabled=False)
                self.window['Times Rumour Heard'].update(disabled=False)

            if event == 'Rumour Heard':
                # set visualisation type to heard rumour, disable its button
                self.visuals = 'heard rumour'
                self.window['Rumour Heard'].update(disabled=True)
                self.window['Spread Cooldown'].update(disabled=False)
                self.window['Times Rumour Heard'].update(disabled=False)
                self.window['None'].update(disabled=False)

            if event == 'Times Rumour Heard':
                # set visualisation type to got_rumour, disable its button
                self.visuals = 'got_rumour'
                self.window['Times Rumour Heard'].update(disabled=True)
                self.window['Rumour Heard'].update(disabled=False)
                self.window['Spread Cooldown'].update(disabled=False)
                self.window['None'].update(disabled=False)

            if event == 'None':
                # set visualisation type to None, disable its button
                self.visuals = 'None'
                self.window['None'].update(disabled=True)
                self.window['Times Rumour Heard'].update(disabled=False)
                self.window['Rumour Heard'].update(disabled=False)
                self.window['Spread Cooldown'].update(disabled=False)
                
            if event == 'Generate Statistics':
                # generate the average spread for reapets of the simulation
                # given the current parameters
                average_spread = 0
                repeats = int(values['repeats'])
                sim_values = self.process_values(values)
                for i in range(repeats):
                    simulation = Sim.Simulation(*sim_values, self.strategy)
                    simulation.run(preprocess=True)
                    average_spread += simulation.get_stats()

                average_spread = average_spread/repeats
                sg.popup(f"Average Spread: {round(average_spread*100, 2)}%", font=self.AppFont)

            if event == 'Information':
                # start a popup window with information about the program
                sg.popup(self.infotext, font=self.AppFont)

            if event == 'Start Simulation':
                # process user entered parameters
                sim_values = self.process_values(values)

                # invalid values entered, error is printed in the function
                if sim_values == None:
                    continue
                # sim_values = [0.7, 2, 15, 0.7, 0.15, 0.1, 0.05]
                self.start_simulation(sim_values)
            
            if event == 'Strategic Simulation':
                # process user entered parameters
                sim_values = self.process_values(values)

                # invalid values entered, error is printed in the function
                if sim_values == None:
                    continue

                self.start_simulation(sim_values, self.strategy)
                
                
        self.window.close()