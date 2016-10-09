#!/usr/bin/env python

from utilities import panel_size
from time_panel import TimeControlPanel
from pylab import *         #includes arange
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class VolumePanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__( self, parent)        
        # initialize matplotlib stuff
        self.figure = Figure()
        self.canvas = FigureCanvas( self, -1, self.figure )
        self.ax = self.figure.add_subplot(111)

        #print "Top Applications ..."
        self.timeControlPanel = TimeControlPanel(self)


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.timeControlPanel, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.canvas, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.SetSize(panel_size)

        self.add_toolbar()  # comment this out for no toolbar





    def add_toolbar(self):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        if wx.Platform == '__WXMAC__':
             self.SetToolBar(self.toolbar)
        else:
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            self.toolbar.SetSize(wx.Size(fw, th))
            self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()