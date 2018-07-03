import serial
from tkinter import *
import _thread
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt


root = Tk()

class GUI():
    def __init__(self, master):
        master.columnconfigure(0,weight=1)
        master.rowconfigure(1,weight=1)
        self.master = master
        self.master.title("Attitude Tester")
        self.master.geometry('800x600')
        self.master.attributes("-zoomed", False)
        self.createGraph()
        self.plotGraph()
        self.master.bind("<Escape>", self.end_fullscreen)

    def end_fullscreen(self, event=None):
        self.state = False
        sys.exit()

    def createGraph(self):
        self.frame = Frame(self.master)
        self.frame.grid(column=0,row=1,columnspan=4, rowspan=3, sticky=N+W+E+S)
        self.f = Figure( figsize=(8, 7), dpi=80 )
        self.ax0 = self.f.add_axes( (0.05, .15, .90, .80), frameon=False)
        self.ax0.set_xlabel( 'Time (ms)' )
        self.ax0.set_ylabel( 'Thrust (N)' )
        self.ax0.grid(color='r',linestyle='-', linewidth=2)
        self.sliderAxis = self.f.add_axes([0.15, 0.05, 0.80, 0.025])
        #self.ax0.plot(np.max(np.random.rand(100,10)*10,axis=1),"r-")
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        # self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.slider = Slider(self.sliderAxis, "X Orientation", -90, 90, valinit=0, valstep=1)
        self.slider.on_changed(self.updateData)
        # self.toolbar.grid(column = 0, row = 2, columnspan=2)
        self.toolbar.update()

    def plotGraph(self):
        xData = []
        yData = []
        for i in range(0,5):
            xData.append(i)
            yData.append(self.slider.val)
        self.line, = self.ax0.plot(xData,yData)
        self.line.set_color("blue")
        self.canvas.draw()

    def updateData(self, val):
        xData = []
        yData = []
        self.line.set_linestyle('')
        for i in range(0,5):
            xData.append(i)
            yData.append(val)
        self.line, = self.ax0.plot(xData,yData)
        self.line.set_color("blue")
        self.canvas.draw()

def main():
    graph = GUI(root)
    root.mainloop()

main()
