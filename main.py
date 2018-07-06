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


orientationData = []
root = Tk()

class SyntaxParser():
    prevTime = 0
    prevSyntax = None
    START_LINE = '@{'
    END_LINE = '}@'
    TIMING = ';'
    GYRO_SYNTAX = ["GX:", "GY:", "GZ:", "TS:"]
    ACCEL_SYNTAX = ["AX:", "AY:", "AZ:", "TS:"]
    ORIENTATION_SYNTAX = ["OX:", "OY:", "OZ:", "TS:"]
    PRESSURE_SYNTAX = ["PS:", "TS:"]
    ALTITUDE_SYNTAX = ["PA:", "TS:"]

    def parseLine(self, line):
        print(line)
        toAppend = 0.0
        syntax = self.getSyntax(line)
        data = []
        startIndex = line.index(self.START_LINE)
        endIndex = line.index(self.END_LINE)
        if self.goodLine(line):
            for i in range(0, len(syntax)):
                if(i < len(syntax)-1):
                    toAppend = float(line[line.index(syntax[i])+3:line.index(syntax[i+1])-1])
                else:
                    toAppend = float(line[line.index(syntax[i])+3:endIndex])
                    if toAppend <= self.prevTime and syntax == self.prevSyntax:
                        return None
                    self.prevTime = toAppend
                data.append(toAppend)
                self.prevSyntax = syntax
            return data
        else: return None

    def getSyntax(self, line):
        startIndex = line.index(self.START_LINE)
        testSyntax = line[startIndex+2:startIndex+5]
        if(testSyntax == self.GYRO_SYNTAX[0]):
            return self.GYRO_SYNTAX
        elif(testSyntax == self.ACCEL_SYNTAX[0]):
            return self.ACCEL_SYNTAX
        elif(testSyntax == self.ORIENTATION_SYNTAX[0]):
            return self.ORIENTATION_SYNTAX
        elif(testSyntax == self.PRESSURE_SYNTAX[0]):
            return self.PRESSURE_SYNTAX
        elif(testSyntax == self.ALTITUDE_SYNTAX[0]):
            return self.ALTITUDE_SYNTAX

    def goodLine(self, line):
        startIndex = line.index(self.START_LINE)
        endIndex = line.index(self.END_LINE)
        syntax = self.getSyntax(line)
        timingCount = self.getTimingCount(line)
        if startIndex is not None and endIndex is not None and syntax is not None:
            if timingCount is len(syntax)-1:
                return True
        return False

    def getTimingCount(self, line):
        count = 0;
        for i in line:
            if i is self.TIMING:
                count += 1
        return count

class ArduinoCommunicator():
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200)

    def readData(self):
        return str(self.ser.readline())

    def isAvailable(self):
        return self.ser.is_open

    def writeData(self, data):
        self.ser.write(data + "\n")

    def kill(self):
        self.ser.close()

class GUI():
    ox = []
    oy = []
    oz = []
    ts = []
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
        self.slider.on_changed(self.plotGraph)
        self.slider1 = Slider(self.sliderAxis1, "Y Orientation", -90, 90, valinit=0, valstep=1)
        self.slider1.on_changed(self.plotGraph)
        self.slider2 = Slider(self.sliderAxis2, "Z Orientation", -90, 90, valinit=0, valstep=1)
        self.slider2.on_changed(self.plotGraph)
        # self.toolbar.grid(column = 0, row = 2, columnspan=2)
        self.toolbar.update()

    def plotGraph(self):
        xData = []
        yData = []
        zData = []
        for i in range(0,len(self.ts)):
            xData.append(self.slider.val)
            yData.append(self.slider1.val)
            zData.append(self.slider2.val)
        comms.writeData(self.slider.val)
        comms.writeData(self.slider1.val)
        comms.writeData(self.slider2.val)
        self.line, = self.ax0.plot(self.ts,xData)
        self.line.set_color("blue")
        self.line1, = self.ax1.plot(self.ts,yData)
        self.line1.set_color("blue")
        self.line2, = self.ax2.plot(self.ts,zData)
        self.line2.set_color("blue")
        self.addOrientationData()
        self.l = self.ax0.plot(self.ts, self.ox)
        self.l.set_color("black")
        self.l1 = self.ax1.plot(self.ts, self.oy)
        self.l1.set_color("black")
        self.l2 = self.ax2.plot(self.ts, self.oy)
        self.l2.set_color("black")
        self.canvas.draw()

    def addOrientationData(self):
        self.ox = []
        self.oy = []
        self.oz = []
        self.ts = []
        for i in orientationData:
            self.ox.append(i[0])
            self.oy.append(i[1])
            self.oz.append(i[2])
            self.ts.append(i[3])

def runArduino():
    print("start thread")
    parser = SyntaxParser()
    f = comms.readData()
    while comms.isAvailable():
        if parser.START_LINE in f and parser.END_LINE in f:
            sampleData = parser.parseLine(f)
            if(sampleData != None):
                orientationData.append(sampleData)
                graph.plotGraph()
            f = comms.readData()
        else:
            f = comms.readData()

def main():
    _thread.start_new_thread(runArduino, ())
    root.mainloop()

comms = ArduinoCommunicator("/dev/ttyACM0")
graph = GUI(root)
main()
