import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt

# Note the matplot tk canvas import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self) -> None:
    # VARS CONSTS:
        _VARS = {'window': False}   
        AppFont = 'Any 16'
        sg.theme('LightGrey')
        
        layout = [[sg.Canvas(key='figCanvas')],
                [sg.Button('Exit', font=AppFont)]]
        _VARS['window'] = sg.Window('Such Window',
                                    layout,
                                    finalize=True,
                                    resizable=True,
                                    element_justification="right")
        
        # MAIN LOOP
        while True:
            event, values = _VARS['window'].read(timeout=200)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == 'Set Parameters':
                pass
        _VARS['window'].close()


    def draw_figure(canvas, figure):
        # draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig)
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

# \\  -------- PYSIMPLEGUI -------- //




# \\  -------- PYSIMPLEGUI -------- //


# \\  -------- PYPLOT -------- //

# Make synthetic data
dataSize = 1000
xData = np.random.randint(100, size=dataSize)
yData = np.linspace(0, dataSize, num=dataSize, dtype=int)
# make fig and plot
fig = plt.figure()
plt.plot(xData, yData)
# Instead of plt.show

# \\  -------- PYPLOT -------- //

