import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sim
import time
import os
# Note the matplot tk canvas import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self) -> None:

        sg.theme('DarkAmber')

        self.AppFont = 'Any 18'
        self.shape = (800, 800)
        self.matrix_shape = (100,100)
        
        # background_color='red',
        layout = [[sg.Text(key="show_iter")],
                    [sg.Image(key='frame')],
                    [sg.Text('enter parameters:')],
                    [sg.Text('p:'),sg.Input(key='p')],
                    [sg.Text('l:'),sg.Input(key='l')],
                    [sg.Text('number of iterations:'), sg.Input(key='iter')],
                    [sg.Text('susceptibility ratio:')],
                    [sg.Text('s1'), sg.Input(key='s1'), sg.Text('s2'), sg.Input(key='s2'),sg.Text('s3'), sg.Input(key='s3'), sg.Text('s4'), sg.Input(key='s4')],
                    [sg.Button('Start Simulation')],
                    [sg.Button('Exit', font=self.AppFont)]]
        
        self.window = sg.Window('Rumour Spreading Simulation',
                                    layout,
                                    finalize=True,
                                    resizable=True,
                                    element_justification="left")
        
        self.start()
       

    def start(self):
        # MAIN LOOP
        while True:
            event, values = self.window.read(timeout=200)
           
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if event == 'Start Simulation':
                # process user entered parameters
                sim_values = [float(values['p']), int(values['l']), int(values['iter']),
                               float(values['s1']), float(values['s2']), float(values['s3']), float(values['s4'])]
                
                 
                simulation = sim.Simulation(*sim_values)
                frames = simulation.run()
                
                for i in range(frames.shape[0]):
                    self.draw_frame(frames[i], i)
                        
        self.window.close()
        
        

    def draw_frame(self, frame, iteration):
        
        resized_frame = np.ndarray(shape=self.shape)
        rectangle_side = int(self.shape[0]/self.matrix_shape[0])
        for i in range(0, self.shape[0]-rectangle_side, rectangle_side ):
            for j in range(0, self.shape[1]-rectangle_side, rectangle_side):
                # Draw the matrix on the graph
                resized_frame[i:i+rectangle_side, j:j+rectangle_side] = frame[int(i/rectangle_side), int(j/rectangle_side)]
                
        plt.imsave("frame.png", resized_frame, cmap='inferno')
        self.window['show_iter'].update(f"iteration number {iteration}")
        self.window['frame'].update("frame.png")
        time.sleep(0.05)
        self.window.refresh()
        try:
            os.remove("frame.png")
        except:
            pass
        
        
                
gui = Gui()
# gui.draw_figure(fig)
