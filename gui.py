import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import sim

# Note the matplot tk canvas import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self) -> None:
    # VARS CONSTS:
        self.AppFont = 'Any 18'
        sg.theme('DarkAmber')
        
        layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0,0), graph_top_right=(400, 400), background_color='red', key='graph')],
                    # [sg.Text('enter parameters:')],
                    # [sg.Text('p:'),sg.Input(key='p')],
                    # [sg.Text('l:'),sg.Input(key='l')],
                    # [sg.Text('number of iterations:'), sg.Input(key='iter')],
                    # [sg.Text('susceptibility ratio:')],
                    # [sg.Text('s1'), sg.Input(key='s1'), sg.Text('s2'), sg.Input(key='s2'),sg.Text('s3'), sg.Input(key='s3'), sg.Text('s4'), sg.Input(key='s4')],
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
                # sim_values = [float(values['p']), int(values['l']), int(values['iter']),
                #                float(values['s1']), float(values['s2']), float(values['s3']), float(values['s4'])]
                
                simulation = sim.Simulation(0.6, 2, 100, 0.25, 0.25, 0.25, 0.25)

                frames = simulation.run()
                self.draw_simulation(frames)

                                        
        self.window.close()
        

    def draw_simulation(self, frames):
        for frame in frames:
            graph = self.window['graph']

            # Draw the matrix on the graph
            graph.DrawRectangle((25,300), (100,280), line_color='red')
            for i in range():
                pass



# Make synthetic data
dataSize = 1000
xData = np.random.randint(100, size=dataSize)
yData = np.linspace(0, dataSize, num=dataSize, dtype=int)
# make fig and plot
fig = plt.figure()
plt.plot(xData, yData)
# Instead of plt.show

gui = Gui()
# gui.draw_figure(fig)
