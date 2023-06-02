from matplotlib.figure import Figure
import numpy as np
# class based on https://stackoverflow.com/questions/11551049/matplotlib-plot-zooming-with-scroll-wheel
class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = np.empty([2])
        self.cur_ylim = np.empty([2])
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            if np.any(self.cur_xlim) and np.any(self.cur_ylim):  # new
                self.cur_xlim = ax.get_xlim() # new
                self.cur_ylim = ax.get_ylim() # new
            else:
                print(f'limits were already set self.cur_xlim={self.cur_xlim} self.cur_ylim={self.cur_ylim}')
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
            new_width = (self.cur_xlim[1] - self.cur_xlim[0]) * scale_factor # new
            new_height = (self.cur_ylim[1] - self.cur_ylim[0]) * scale_factor # new
            relx = (self.cur_xlim[1] - xdata)/(self.cur_xlim[1] - self.cur_xlim[0]) # new
            rely = (self.cur_ylim[1] - ydata)/(self.cur_ylim[1] - self.cur_ylim[0]) # new
            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            ax.figure.canvas.draw()
        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)
        return zoom
    def pan_factory(self, ax):
        def onPress(event):
            if event.button == 1:return
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press
        def onRelease(event):
            if event.button == 1:return
            self.press = None
            ax.figure.canvas.draw()
        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)
            ax.figure.canvas.draw()
        fig = ax.get_figure() # get the figure of interest
        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)
        return onMotion