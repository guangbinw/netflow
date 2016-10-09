#!/usr/bin/env python

#from time_panel import ants_start_date
from utilities import panel_size
from utilities import getRowset
from time_panel import TimeControlPanel
from pylab import *         #includes arange
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


class TopTalkersPlotPanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__( self, parent)

        limit = '8'
        sql = "select dstaddr as dst_addr, sum(octets)/1024 from flow where dstaddr like '192.168.0%' group by dstaddr order by sum(octets) desc limit " + limit
        sql_total_volume = "select sum(octets)/1048576 from flow where dstaddr like '192.168.0%'"

        self.figure = Figure()
        self.canvas = FigureCanvas( self, -1, self.figure )
        self.ax = self.figure.add_subplot(111)
        #self.ax = self.figure.add_subplot(111, polar=True)
        self.ax.yaxis.grid(True, which='major')
        self.ax.grid(True)

        self.timeControlPanel = TimeControlPanel(self)
        self.start_date =  self.timeControlPanel.datepicker_end_date.GetValue()
   
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.timeControlPanel, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.canvas, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        #self.sizer.Fit (parent)
        self.Fit()
        self.SetSize(panel_size)
        self.add_toolbar()  # comment this out for no toolbar

        #self.Bind(wx.EVT_BUTTON, self.eventDatesChanged, self.buttonDatesChanged)
        self.Bind(wx.EVT_BUTTON, self.eventDatesChanged)

        #EVT_PAINT(self, self.OnPaint)


        rowset = getRowset(sql)
        total_traffic_volume = getRowset(sql_total_volume)

        self.ax.set_title("Top Talkers - Total Volume: %s MB" % total_traffic_volume[0])
        labels = []
        host_labels = [""] #for offsetting the -1 appearing on the graph
        #host_labels = []
        traffic_volume = []
        for row in rowset:
            labels.append(str(row[0]))
            host_labels.append(str(row[0]))
            traffic_volume.append(row[1])

        #Plot the horizontal bar chart
        self.ax.barh(arange(len(labels)), traffic_volume, align='center')
        self.ax.set_ylabel('Hosts')
        self.ax.set_xlabel('Volume (Kilobytes)')
        self.ax.set_yticklabels(host_labels)

        #print labels
        for label in self.ax.yaxis.get_ticklabels():
            label.set_color('blue')
        #self.Pack()

    def OnPaint(self, event):
        self.canvas.draw()

    def eventDatesChanged(self, event):
        self.start_date =  self.timeControlPanel.datepicker_start_date.GetValue()
        #print "Top talkers, eventDatesChanged...start_date = ", self.start_date
        #event.Skip()

    def eventTimeChoiceChanged(self, event):
        print "Top talkers eventTimeChoiceChanged' Time selected"
        event.Skip()

    def add_toolbar(self):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        if wx.Platform == '__WXMAC__':
            # Mac platform (OSX 10.3, MacPython) does not seem to cope with
            # having a toolbar in a sizer. This work-around gets the buttons
            # back, but at the expense of having the toolbar at the top
            self.SetToolBar(self.toolbar)
        else:
            # On Windows platform, default window size is incorrect, so set
            # toolbar width to figure width.
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            # By adding toolbar in sizer, we are able to put it at the bottom
            # of the frame - so appearance is closer to GTK version.
            # As noted above, doesn't work for Mac.
            self.toolbar.SetSize(wx.Size(fw, th))
            self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()


