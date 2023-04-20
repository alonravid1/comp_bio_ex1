import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import sim
import time
import os


class Gui:
    def __init__(self):
        # setting general GUI properties
        sg.theme('DarkAmber')

        self.AppFont = 'Any 12'
        self.shape = (500, 500)
        self.matrix_shape = (100,100)
        
        # set main window's layout
        self.main_layout = [
            [sg.Text('enter parameters:', font=self.AppFont)],
            [sg.Text('p:',font=self.AppFont), sg.Input(key='p', size=(15,1), font=self.AppFont, default_text='0.85')],
            [sg.Text('l:',font=self.AppFont), sg.Input(key='l', size=(15,1), font=self.AppFont, default_text='2')],
                    
            [sg.Text('number of iterations:', font=self.AppFont),
                sg.Input(key='iter', size=(15,1), font=self.AppFont, default_text='100')],
            
            [sg.Text('susceptibility distribution:', font=self.AppFont)],
            
            [sg.Text('s1',font=self.AppFont), sg.Input(key='s1', size=(15,1), font=self.AppFont, default_text='0.7'),
             sg.Text('s2',font=self.AppFont), sg.Input(key='s2', size=(15,1), font=self.AppFont, default_text='0.15'),
             sg.Text('s3',font=self.AppFont), sg.Input(key='s3', size=(15,1), font=self.AppFont, default_text='0.1'),
             sg.Text('s4',font=self.AppFont), sg.Input(key='s4', size=(15,1), font=self.AppFont, default_text='0.05')
            ],
            
            [sg.Button('Information', font=self.AppFont)],
            [sg.Button('Start Simulation', font=self.AppFont)],
            [sg.Button('Exit', font=self.AppFont)]
            ]
        
        self.infotext = """welcome to the rumour spreading simulator,
        please enter the following parameters as follows:
        * P - portion of the cells that are inhibited. Enter a number between 0 and 1.
        * L - spread limiter, after spreading the rumour a cell cannot spread it again for L iterations. Enter a positive integer.
        * Number of iterations - how many iterations the simulation will run. Enter a positive integer.
        * Suciptibilty level ratios - defined in the parameters s1, s2, s3 and s4, the parameters represent a distribution function whose values are 1, 2/3, 1/3, 0 respectively. The values represent the probabilty that a cell will believe a rumour and then spread it upon hearing it.
        enter 4 numbers between 0 and 1, summing up to 1.
        
        Upon clicking start simulation the program will take a few seconds to first
        run the simulation and then display it. If you close it before it finishes
        it will cause the gui to crash and you will need to close it.
        """
        # self.start()
        
    def create_sim_layout(self):
        """
        pysimplegui cannot reuse a layout, generating a new
        layout with new element objects is the solution, rather
        than trying to create a template and starting to work on
        deep copying the very flexible nested arrays of elements.
        """
        fresh_layout = [[sg.Text(key="show_iter", font=self.AppFont)],
                    [sg.Image(key='frame'),
                    [sg.Button('Close', font=self.AppFont, disabled=True)]]]
        
        return fresh_layout
        
           
    def draw_frame(self, window, frame, iteration,):
        """
        function resizes the given frame to be bigger, saves it
        as an image and then shows it on the GUI for 0.05 of a second
        """
        
        resized_frame = np.ndarray(shape=self.shape)
        horizental_side = int(self.shape[0]/self.matrix_shape[0])
        vercitcal_side = int(self.shape[1]/self.matrix_shape[1])
        # rectangle_side = int(self.shape[0]/self.matrix_shape[0])
        for i in range(0, self.shape[0]-horizental_side, horizental_side ):
            for j in range(0, self.shape[1]-vercitcal_side, vercitcal_side):
                # Draw the matrix on the graph
                resized_frame[i:i+horizental_side, j:j+vercitcal_side] = frame[int(i/horizental_side), int(j/vercitcal_side)]
                
        plt.imsave("frame.png", resized_frame, cmap='inferno')
        window['show_iter'].update(f"iteration number {iteration}")
        window['frame'].update("frame.png")
        time.sleep(0.05)        
        window.refresh()

    def start_simulation(self, sim_values):
        """
        creates the new simulation window, runs the simulation
        to get all itertion frames, and then show each one
        using draw_frame(), afterwhich it gives the user the option to
        close the window whenever they'd like
        """
        window = sg.Window('Rumour Spreading Simulation',
                                    self.create_sim_layout(),
                                    finalize=True,
                                    resizable=True,
                                    element_justification="left")
        
        
        
        # run the simulation, save the generated frames
        simulation = sim.Simulation(*sim_values)
        frames = simulation.run()
        
        # set window to middle of screen
        screen_width, screen_height = window.get_screen_dimensions()
        win_width, win_height = window.size
        x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
        window.move(x, y)
        
        # draw first frame and then move the
        # window to the middle of the screen
        self.draw_frame(window, frames[0], 0)
        screen_width, screen_height = window.get_screen_dimensions()
        win_width, win_height = window.size
        x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
        window.move(x, y)
        
        # draw the simulation frames
        for i in range(1, frames.shape[0]):
            self.draw_frame(window, frames[i], i)
            
        # show close button for simulation    
        window['Close'].update(disabled=False)
        
        event = 'blah'
        while event != sg.WIN_CLOSED and event != 'Close':
            event, values = window.read(timeout=200)
            
        window.close()
            
        # delete frame file
        try:
            os.remove("frame.png")
        except:
            pass
                
                
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
            
            if event == 'Information':
                sg.popup(self.infotext)
            if event == 'Start Simulation':
                # process user entered parameters
                try:
                    sim_values = [float(values['p']), int(values['l']), int(values['iter']),
                                float(values['s1']), float(values['s2']), float(values['s3']), float(values['s4'])]
                    
                    # check all values are positive
                    if any(value < 0 for value in sim_values):
                        sg.popup('Values cannot be negative')
                        continue
                    if (sim_values[1] < 1 or sim_values[2] <1):
                        sg.popup('both l and number of iterations must be at least 1')
                        continue
                    if sum(sim_values[3:]) != 1 :
                        sg.popup('distribution probability values must add up to 1')
                        continue
                    if sim_values[0] > 1 :
                        sg.popup('P value must be between 0 and 1')
                        continue
                    
                except:
                    sg.popup('Error parsing input')
                    continue
                
                # sim_values = [0.7, 2, 15, 0.7, 0.15, 0.1, 0.05]
                self.start_simulation(sim_values)
                
                
        self.window.close()
        
        


        
        
        
      

if __name__ == '__main__':
    gui = Gui()
    gui.start()