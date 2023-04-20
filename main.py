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
        self.shape = (500, 300)
        self.matrix_shape = (100,100)
        
        # set main window's layout
        self.main_layout = [
            [sg.Text('enter parameters:', font=self.AppFont)],
            [sg.Text('p:',font=self.AppFont), sg.Input(key='p', size=(15,1), font=self.AppFont, default_text='0.7')],
            [sg.Text('l:',font=self.AppFont), sg.Input(key='l', size=(15,1), font=self.AppFont, default_text='2')],
                    
            [sg.Text('number of iterations:', font=self.AppFont),
                sg.Input(key='iter', size=(15,1), font=self.AppFont, default_text='100')],
            
            [sg.Text('susceptibility distribution:', font=self.AppFont)],
            
            [sg.Text('s1',font=self.AppFont), sg.Input(key='s1', size=(15,1), font=self.AppFont, default_text='0.7'),
             sg.Text('s2',font=self.AppFont), sg.Input(key='s2', size=(15,1), font=self.AppFont, default_text='0.15'),
             sg.Text('s3',font=self.AppFont), sg.Input(key='s3', size=(15,1), font=self.AppFont, default_text='0.1'),
             sg.Text('s4',font=self.AppFont), sg.Input(key='s4', size=(15,1), font=self.AppFont, default_text='0.05')
            ],
            
            [sg.Button('Start Simulation', font=self.AppFont)],
            [sg.Button('Exit', font=self.AppFont)]
            ]
        
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
        # horizental_side = int(self.shape[0]/self.matrix_shape[0])
        # rectangle_horiz = int(self.shape[0]/self.matrix_shape[0])
        rectangle_side = int(self.shape[0]/self.matrix_shape[0])
        for i in range(0, self.shape[0]-rectangle_side, rectangle_side ):
            for j in range(0, self.shape[1]-rectangle_side, rectangle_side):
                # Draw the matrix on the graph
                resized_frame[i:i+rectangle_side, j:j+rectangle_side] = frame[int(i/rectangle_side), int(j/rectangle_side)]
                
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
        simulation = sim.Simulation(*sim_values)
        frames = simulation.run()
        
        for i in range(frames.shape[0]):
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