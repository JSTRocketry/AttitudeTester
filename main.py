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
        self.ax0 = self.f.add_axes([.05, .625, .4, .35], frameon=False, label='X Orientation')
        self.ax0.set_xlabel( 'Time (ms)' )
        self.ax0.set_ylabel( 'Degree' )
        self.ax0.grid(color='r', linestyle='-', linewidth=2)
        self.ax1 = self.f.add_axes([.55, .625, .4, .35], frameon=False, label='Y Orientation')
        self.ax1.set_xlabel('Time (ms)')
        self.ax1.set_ylabel('Degree')
        self.ax1.grid(color='r', linestyle='-', linewidth=2)
        self.ax2 = self.f.add_axes([.3, .125, .4, .35], frameon=False, label='Z Orientation')
        self.ax2.set_xlabel('Time (ms)')
        self.ax2.set_ylabel('Degree')
        self.ax2.grid(color='r', linestyle='-', linewidth=2)
        self.sliderAxis = self.f.add_axes([.075, .525, .325, .025])
        self.sliderAxis1 = self.f.add_axes([.6, .525, .325, .025])
        self.sliderAxis2 = self.f.add_axes([.35, .025, .325, .025])
        #self.ax0.plot(np.max(np.random.rand(100,10)*10,axis=1),"r-")
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        # self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.slider = Slider(self.sliderAxis, "X Orientation", -90, 90, valinit=0, valstep=1)
        self.slider.on_changed(self.updateData0)
        self.slider1 = Slider(self.sliderAxis1, "Y Orientation", -90, 90, valinit=0, valstep=1)
        self.slider1.on_changed(self.updateData1)
        self.slider2 = Slider(self.sliderAxis2, "Z Orientation", -90, 90, valinit=0, valstep=1)
        self.slider2.on_changed(self.updateData2)
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
        self.line1, = self.ax1.plot(xData,yData)
        self.line1.set_color("blue")
        self.line2, = self.ax2.plot(xData,yData)
        self.line2.set_color("blue")
        self.canvas.draw()

    def updateData0(self, val):
        xData = []
        yData = []
        self.line.set_linestyle('')
        for i in range(0,5):
            xData.append(i)
            yData.append(val)
        self.line, = self.ax0.plot(xData,yData)
        self.line.set_color("blue")
        self.canvas.draw()

    def updateData1(self, val):
        xData = []
        yData = []
        self.line1.set_linestyle('')
        for i in range(0,5):
            xData.append(i)
            yData.append(val)
        self.line1, = self.ax1.plot(xData,yData)
        self.line1.set_color("blue")
        self.canvas.draw()

    def updateData2(self, val):
        xData = []
        yData = []
        self.line2.set_linestyle('')
        for i in range(0,5):
            xData.append(i)
            yData.append(val)
        self.line2, = self.ax2.plot(xData,yData)
        self.line2.set_color("blue")
        self.canvas.draw()

def main():
    graph = GUI(root)
    root.mainloop()

main()
